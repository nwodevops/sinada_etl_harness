# impl fase-6-oefa

Fecha: 2026-10-13

## Archivos

- `inputs.yaml`: `STG_GS9` a `STG_GS18`, libro `TABLAS SINADA_OEFA v11 - Final`.
- `python/io/leer_h2.py`: claves `OEFA_*`.
- `logica/sinada_denuncias.py`: `_hoja` copia las columnas H2. Bota `COLUMN_*` / `COLUMNA_*` vacías y filas vacías. Sin `ANIO`.
- `python/sinada_campos.py`: `HOJAS_OEFA` dentro de `TABLAS`.
- `init.sh` e `init.bat`: conteo STG y `Oracle RP_SINADA_OEFA_*`.

## Evidencia Linux

`./init.sh` cerró en `HARNESS OK` (2026-10-13). Log: `logs/init_20261013.log`.

- `RP_SINADA_OEFA_REGISTROS`: 3160
- `RP_SINADA_OEFA_SEGUIMIENTO`: 2037
- `RP_SINADA_OEFA_ASIGNACIONES`: 2364
- `RP_SINADA_OEFA_EVALUACION`: 2312 (34 columnas; se fueron `Column 35/36/37`)
- `RP_SINADA_OEFA_VALIDACION`: 2267
- `RP_SINADA_OEFA_DOC_COMUNIC`: 3664
- `RP_SINADA_OEFA_DOC_DERIV`: 2143
- `RP_SINADA_OEFA_VAL_RPTA`: 1808
- `RP_SINADA_OEFA_DOC_REI`: 8
- `RP_SINADA_OEFA_DOC_OCI`: 67 (12 columnas; se fue `Columna 13`)
- `RP_SINADA_DENUNCIAS_DERIVACIONES`: 37061. Excel solo de `RESULTADO`.

## Windows (no corrido desde Linux)

`init.bat` ya exige los mismos conteos. Comprobar en el equipo Windows: `init.bat remote` hasta `HARNESS OK`.
