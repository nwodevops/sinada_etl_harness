# impl fase-7-tipos

Fecha: 2026-10-13

## Archivos

- `python/sinada_campos.py`: `TIPOS`, 60 pares `(tabla, columna)`.
- `python/io/cargar_dw.py`: `DATE` y `NUMBER` en el DDL. Si el tipo no coincide, `DROP` + `CREATE`. El valor que no parsea queda nulo.
- Nombres corregidos del Excel: `FECHA_ENVIO_PROYEC_REITERATIVO`, `DIAS_TRANSCURRIDOS_REITERATIVO`, `FECHA_NOTIFICACION_OCI`, `RP_SINADA_OEFA_ASIGNACIONES`.
- `A_O_DEL_DOCUMENTO`: el año se guarda como 1 de enero.

## Evidencia Linux

`./init.sh` cerró en `HARNESS OK` (2026-10-13). Log: `logs/init_20261013.log`.

Oracle recreó las tablas con campos tipados. Muestra leída después de la carga:

- `FECHA_FIRMA` `DATE`, `PLAZO` `NUMBER`, `ANIO` y `CODIGO_SINADA` `VARCHAR2`
- `FERIADO` `DATE`, `FECHA_INGRESO` `DATE`
- `A_O_DEL_DOCUMENTO` `DATE` = 2026-01-01 (3170 filas)
- `RP_SINADA_OEFA_ASIGNACIONES.PLAZO` sigue `VARCHAR2`
- `NU_COORDENADA_X` y `EFA` siguen `VARCHAR2`

`RP_SINADA_DENUNCIAS_DERIVACIONES`: 37067 filas. Las hojas OEFA crecieron unas filas respecto de la corrida de la mañana.

## Windows (no corrido desde Linux)

`init.bat` no cambió. La conversión vive en `cargar_dw.py`, así que `init.bat remote` la aplica. Comprobar en el equipo Windows.
