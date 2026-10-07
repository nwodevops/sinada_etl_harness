# impl fase-5-catalogos

Fecha: 2026-10-07

## Archivos

- `inputs.yaml`: `STG_GS5_DIRECTORIO`, `STG_GS6_REGISTROS`, `STG_GS7_UBIGEO`, `STG_GS8_FERIADOS`.
- `python/io/leer_h2.py`: `DIR_SEFA`, `CIF_REGISTROS`, `CIF_UBIGEO`, `FERIADOS_SRC`.
- `python/sinada_campos.py`: mapas y `TABLAS`.
- `logica/sinada_denuncias.py`: proyecta las cuatro tablas. `RESULTADO` no cambia.
- `python/io/cargar_dw.py`: recibe tabla y columnas. Full refresh.
- `python/main.py`: una carga por entrada de `TABLAS`. Excel sigue siendo solo `RESULTADO`.
- `init.sh` e `init.bat`: conteo STG y `Oracle RP_SINADA_*`.

## Evidencia Linux

`./init.sh` cerró en `HARNESS OK` (2026-10-07). Log: `logs/init_20261007.log`.

- `STG_GS5_DIRECTORIO`: 2442 filas. `Oracle RP_SINADA_DIRECTORIO_SEFA`: 2442 (`EFA`, `TIPO_EFA`, `TIPO_DOC`)
- `STG_GS6_REGISTROS`: 33502 filas. `Oracle RP_SINADA_REGISTROS`: 33502 (`CODIGO_SINADA`, `FECHA_INGRESO`, `FECHA_REGISTRO`)
- `STG_GS7_UBIGEO`: 34969 filas. `Oracle RP_SINADA_UBIGEO`: 34969
- `STG_GS8_FERIADOS`: 228 filas. `Oracle RP_SINADA_FERIADOS`: 228 (`FERIADO`)
- `Oracle RP_SINADA_DENUNCIAS_DERIVACIONES`: 37059
- Excel `output/resultado.xlsx`: 37059 x 31

## Windows

Corrida completa confirmada el 2026-10-07 en Windows 11 (`D:\Eder\workspace_etl_oefa\sinada_etl_harness`), después de crear `.venv` e instalar `python/requirements.txt`. El primer intento falló en `create_stg.py` con `No module named 'yaml'` porque el venv no viaja en git.
