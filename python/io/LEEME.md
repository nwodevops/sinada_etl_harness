# python/io/ — I/O post-staging (arquetipo mínimo)

Hop (o el smoke) deja datos en H2. Aquí se lee H2 y se escribe el destino demo.

Flujo en `main.py`:
  `leer_h2.py` → `logica/` → `cargar_dw.py` → `escribir_excel.py`

- `leer_h2.py` — `LECTURAS` (contrato de entrada de `logica/`)
- `cargar_stg_sheets.py` — filas Google Sheets → `STG_*` (lo llama el workflow, no `main.py`)
- `cargar_dw.py` — `TRUNCATE` + `INSERT` a Oracle DW y `COUNT(*)`
- `escribir_excel.py` — copia de `RESULTADO` en `output/resultado.xlsx`

No crear `STG_*` aquí. Eso es `python/create_stg.py` / `introspect/`.

No importar este paquete como `import io`: choca con la stdlib.
