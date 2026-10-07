"""Carga full-refresh de RESULTADO a Oracle DW.

DDL si la tabla no existe. Si existe y le faltan columnas, DROP + CREATE.
Si el esquema ya coincide, TRUNCATE + INSERT. El esquema sale de dw_schema()
(DB_ORA_DW_SCHEMA o el usuario en mayúsculas). No va literal en el SQL.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from config import dw_schema, require_live_conn
from sinada_campos import ORACLE_COLUMNS, TABLE

_IDENT_RE = re.compile(r"[A-Z][A-Z0-9_$#]*")
_VARCHAR = 4000


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


def _fila(df: pd.DataFrame, index: int, columnas: list[str]) -> tuple:
    valores = []
    for col in columnas:
        val = df.iat[index, df.columns.get_loc(col)]
        if val is None or (isinstance(val, float) and pd.isna(val)):
            valores.append(None)
            continue
        try:
            if pd.isna(val):
                valores.append(None)
                continue
        except TypeError:
            pass
        text = str(val).strip()
        valores.append(text or None)
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
    col_sql = ",\n".join(
        f"    {col} VARCHAR2({4 if col == 'ANIO' else _VARCHAR} CHAR)"
        for col in columnas
    )
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
                    SELECT COLUMN_NAME
                    FROM ALL_TAB_COLUMNS
                    WHERE OWNER = :owner AND TABLE_NAME = :tname
                    ORDER BY COLUMN_ID
                    """,
                    {"owner": schema, "tname": table},
                )
                actuales = [str(fila[0]) for fila in cur.fetchall()]
                if actuales != columnas:
                    cur.execute(f"DROP TABLE {qualified}")
                    exists = False
                    print(f"Oracle DROP {qualified} (columnas distintas)")
            if not exists:
                cur.execute(create_sql)
                print(f"Oracle DDL {qualified}")
            else:
                cur.execute(f"TRUNCATE TABLE {qualified}")
            filas = [_fila(df, i, columnas) for i in range(len(df))]
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
