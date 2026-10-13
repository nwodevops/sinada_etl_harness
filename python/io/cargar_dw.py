"""Carga full-refresh a Oracle DW.

DDL si la tabla no existe. Si el nombre o el tipo no coinciden, DROP + CREATE.
Si el esquema ya coincide, TRUNCATE + INSERT. El esquema sale de dw_schema()
(DB_ORA_DW_SCHEMA o el usuario en mayúsculas). No va literal en el SQL.
Los campos de TIPOS salen DATE o NUMBER. El resto sigue VARCHAR2.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import pandas as pd

from config import dw_schema, require_live_conn
from sinada_campos import ORACLE_COLUMNS, TABLE, TIPOS

_IDENT_RE = re.compile(r"[A-Z][A-Z0-9_$#]*")
_NUMERO_RE = re.compile(r"-?\d+")
_ANIO_RE = re.compile(r"\d{4}")
_VARCHAR = 4000
_FORMATOS_FECHA = ("%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d")


def _ident(name: str) -> str:
    cleaned = str(name).strip().upper()
    if not _IDENT_RE.fullmatch(cleaned):
        raise ValueError(f"identificador Oracle inválido: {name!r}")
    return cleaned


def _connect(variables: dict[str, str]):
    try:
        import oracledb
    except ImportError as exc:
        raise SystemExit(
            "Falta oracledb. Instala: pip install -r python/requirements.txt"
        ) from exc

    cv = require_live_conn("oracle_dw", variables)
    port = int(cv["port"]) if str(cv["port"]).isdigit() else 1521
    return oracledb.connect(
        user=cv["username"],
        password=cv["password"],
        host=cv["host"],
        port=port,
        service_name=cv["database"],
    )


def _tipo(tabla: str, col: str) -> str:
    return TIPOS.get((tabla, col), "VARCHAR2")


def _ddl(tabla: str, col: str) -> str:
    kind = _tipo(tabla, col)
    if kind == "DATE":
        return "DATE"
    if kind == "NUMBER":
        return "NUMBER"
    if col == "ANIO":
        return "VARCHAR2(4 CHAR)"
    return f"VARCHAR2({_VARCHAR} CHAR)"


def _data_type(tabla: str, col: str) -> str:
    kind = _tipo(tabla, col)
    if kind in ("DATE", "NUMBER"):
        return kind
    return "VARCHAR2"


def _vacio(val) -> bool:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return True
    try:
        if pd.isna(val):
            return True
    except TypeError:
        pass
    return str(val).strip() == ""


def _fecha(text: str, *, anio_solo: bool) -> datetime.date | None:
    for fmt in _FORMATOS_FECHA:
        try:
            parsed = datetime.strptime(text, fmt).date()
        except ValueError:
            continue
        if fmt == "%d/%m/%y" and parsed.year < 2000:
            parsed = parsed.replace(year=parsed.year + 100)
        return parsed
    if anio_solo and _ANIO_RE.fullmatch(text):
        return datetime(int(text), 1, 1).date()
    return None


def _numero(text: str) -> int | None:
    if _NUMERO_RE.fullmatch(text):
        return int(text)
    return None


def _valor(tabla: str, col: str, val):
    if _vacio(val):
        return None
    text = str(val).strip()
    if not text:
        return None
    kind = _tipo(tabla, col)
    if kind == "DATE":
        return _fecha(text, anio_solo=(col == "A_O_DEL_DOCUMENTO"))
    if kind == "NUMBER":
        return _numero(text)
    return text


def _fila(df: pd.DataFrame, index: int, tabla: str, columnas: list[str]) -> tuple:
    valores = []
    for col in columnas:
        val = df.iat[index, df.columns.get_loc(col)]
        valores.append(_valor(tabla, col, val))
    return tuple(valores)


def cargar_dw(
    df: pd.DataFrame,
    root: Path,
    variables: dict[str, str],
    *,
    tabla: str = TABLE,
    columnas: list[str] | None = None,
) -> int:
    del root  # la conexión sale de project-config, no de una ruta
    columnas = list(ORACLE_COLUMNS if columnas is None else columnas)
    if list(df.columns) != columnas:
        raise ValueError(
            f"{tabla} no tiene las columnas Oracle esperadas. "
            f"recibidas={list(df.columns)}"
        )

    schema = _ident(dw_schema(variables))
    table = _ident(tabla)
    qualified = f"{schema}.{table}"
    col_sql = ",\n".join(f"    {col} {_ddl(tabla, col)}" for col in columnas)
    esperados = [_data_type(tabla, col) for col in columnas]
    create_sql = f"CREATE TABLE {qualified} (\n{col_sql}\n)"
    insert_sql = (
        f"INSERT INTO {qualified} ("
        + ", ".join(columnas)
        + ") VALUES ("
        + ", ".join(f":{i}" for i in range(1, len(columnas) + 1))
        + ")"
    )

    conn = _connect(variables)
    try:
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT COUNT(*)
                FROM ALL_TABLES
                WHERE OWNER = :owner AND TABLE_NAME = :tname
                """,
                {"owner": schema, "tname": table},
            )
            exists = int(cur.fetchone()[0]) > 0
            if exists:
                cur.execute(
                    """
                    SELECT COLUMN_NAME, DATA_TYPE
                    FROM ALL_TAB_COLUMNS
                    WHERE OWNER = :owner AND TABLE_NAME = :tname
                    ORDER BY COLUMN_ID
                    """,
                    {"owner": schema, "tname": table},
                )
                actuales = [(str(fila[0]), str(fila[1])) for fila in cur.fetchall()]
                if actuales != list(zip(columnas, esperados)):
                    cur.execute(f"DROP TABLE {qualified}")
                    exists = False
                    print(f"Oracle DROP {qualified} (esquema distinto)")
            if not exists:
                cur.execute(create_sql)
                print(f"Oracle DDL {qualified}")
            else:
                cur.execute(f"TRUNCATE TABLE {qualified}")
            filas = [_fila(df, i, tabla, columnas) for i in range(len(df))]
            if filas:
                cur.executemany(insert_sql, filas)
            cur.execute(f"SELECT COUNT(*) FROM {qualified}")
            total = int(cur.fetchone()[0])
        finally:
            cur.close()
        conn.commit()
    finally:
        conn.close()

    if total != len(df):
        raise SystemExit(
            f"Oracle {qualified}: COUNT(*)={total} distinto de RESULTADO={len(df)}"
        )
    if total == 0:
        raise SystemExit(f"Oracle {qualified}: COUNT(*)=0")
    print(f"Oracle {table}: {total} filas (COUNT(*))")
    return total
