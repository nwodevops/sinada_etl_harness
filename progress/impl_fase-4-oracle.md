# impl fase-4-oracle (cubre fases 1–4)

Fecha: 2026-10-05

## Archivos

- `switch-env.sh`, `switch-env.ps1`: overlay `DB_ORA_DW_*` desde `docs/credenciales/<env>.txt`. No copia `SysPassword`. Esquema = línea `Schema` o usuario en mayúsculas.
- `inputs.yaml`: `STG_GS1_SINADA_DERIV` (2020) y `STG_GS2_SINADA_DERIV` (2021), hoja `Derivaciones`.
- `python/io/cargar_stg_sheets.py`: gspread → H2, 1:1.
- `logica/sinada_denuncias.py`: 26 campos + `ANIO`. Descarta filas vacías en esos 26.
- `python/io/cargar_dw.py`: DDL si falta, si no `TRUNCATE` + `INSERT`, luego `COUNT(*)`.
- `workflows/wf_main.hwf` y `workflows/wf_main_windows.hwf`.
- `init.sh` escribe `logs/init_YYYYMMDD.log`.
- Espejo Windows: `init.bat`, `scripts/step_*.bat`, `run_wf_main.bat`.

## Evidencia Linux

Corrida previa a `./init.sh`:

- `STG_GS1_SINADA_DERIV`: 46 columnas, 2890 filas
- `STG_GS2_SINADA_DERIV`: 52 columnas, 3840 filas
- `RESULTADO`: 6384 filas x 28 columnas (se fueron las filas vacías en los 26 campos)
- `Oracle DDL` + `COUNT(*)` = 6384
- Excel `output/resultado.xlsx`

`./init.sh` cerró en `HARNESS OK` (2026-10-05). La segunda pasada no recreó la tabla: `TRUNCATE` + `INSERT`, `COUNT(*)` = 6384. Log: `logs/init_20261005.log`.

## Windows (no corrido desde Linux)

Comprobar en el equipo Windows:

1. `powershell -ExecutionPolicy Bypass -File switch-env.ps1 remote`
2. `init.bat remote` → `HARNESS OK` y `logs/init_YYYYMMDD.log`
3. Conteos STG > 0 y `COUNT(*)` de `RP_SINADA_DENUNCIAS_DERIVACIONES` en el esquema de `docs/credenciales/remote.txt`
4. Programador de tareas → `run_wf_main.bat`
