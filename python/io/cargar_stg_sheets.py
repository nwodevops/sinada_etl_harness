#!/usr/bin/env python3
"""Carga 1:1 de fuentes sheets de inputs.yaml hacia STG_* en H2.

create_stg.py ya creó el DDL (todos los headers, VARCHAR). Aquí entran las filas.
No homologa: eso es logica/.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = HERE.parent
if str(PY) not in sys.path:
    sys.path.insert(0, str(PY))

from config import load_sources, load_vars, project_root  # noqa: E402
from h2_conn import connect_h2  # noqa: E402
from introspect.h2_ddl import sanitize_ident  # noqa: E402

BATCH = 400


def _sheet_columns(headers: list[str]) -> list[tuple[int, str]]:
    used: set[str] = set()
    cols: list[tuple[int, str]] = []
    for i, header in enumerate(headers):
        if header is None or str(header).strip() == "":
            continue
        cols.append((i, sanitize_ident(str(header), used)))
    return cols


def _cell(raw: list[str], index: int):
    if index >= len(raw):
        return None
    text = "" if raw[index] is None else str(raw[index]).strip()
    return text or None


def _h2_columns(cur, table: str) -> list[str]:
    cur.execute(
        """
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'PUBLIC' AND UPPER(TABLE_NAME) = ?
        ORDER BY ORDINAL_POSITION
        """,
        [table.upper()],
    )
    return [str(row[0]).upper() for row in cur.fetchall()]


def cargar_sheets(root: Path, variables: dict[str, str]) -> dict[str, int]:
    try:
        import gspread
    except ImportError as exc:
        raise SystemExit(
            "Falta gspread. Instala: pip install -r python/requirements.txt"
        ) from exc

    secret = root / "client_secret.json"
    if not secret.is_file():
        raise FileNotFoundError(f"No se encuentra {secret} (service account Google, gitignored)")

    sources = [src for src in load_sources(root, variables) if src["type"] == "sheets"]
    if not sources:
        raise SystemExit("inputs.yaml no declara fuentes type: sheets")

    gc = gspread.service_account(filename=str(secret))
    conteos: dict[str, int] = {}
    conn = connect_h2(root, variables)
    try:
        cur = conn.cursor()
        try:
            for src in sources:
                table = src["stg_table"]
                key = (src.get("spreadsheet_key") or "").strip()
                worksheet = src.get("worksheet")
                if not key or not worksheet:
                    raise ValueError(f"{table}: falta spreadsheet_key o worksheet")
                book = gc.open_by_key(key)
                sheet = book.worksheet(str(worksheet))
                values = sheet.get_all_values()
                if not values:
                    raise ValueError(f"{table}: hoja {worksheet!r} vacía")
                mapped = _sheet_columns(values[0])
                if not mapped:
                    raise ValueError(f"{table}: fila 1 sin headers")
                expected = _h2_columns(cur, table)
                got = [name for _, name in mapped]
                if got != expected:
                    raise ValueError(
                        f"{table}: headers de la hoja no coinciden con el DDL H2. "
                        f"Vuelve a correr create_stg.py. "
                        f"hoja={len(got)} columnas, H2={len(expected)}"
                    )
                rows = [
                    tuple(_cell(raw, idx) for idx, _name in mapped)
                    for raw in values[1:]
                ]
                cur.execute(f"DELETE FROM {table}")
                cols_sql = ", ".join(f'"{name}"' for _idx, name in mapped)
                placeholders = ", ".join(["?"] * len(mapped))
                sql = f"INSERT INTO {table} ({cols_sql}) VALUES ({placeholders})"
                for start in range(0, len(rows), BATCH):
                    cur.executemany(sql, rows[start : start + BATCH])
                conteos[table] = len(rows)
                print(f"{table}: {len(rows)} filas")
        finally:
            cur.close()
        conn.commit()
    finally:
        conn.close()
    return conteos


def main() -> int:
    root = project_root()
    variables = load_vars(root)
    cargar_sheets(root, variables)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
