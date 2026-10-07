# Contrato logica/ (arquetipo mínimo)

## Flujo

```
python/main.py
  → io/leer_h2.py          (H2 → DataFrames)
  → logica/*.py            (un solo archivo)
  → io/cargar_dw.py        (Oracle DW, full refresh)
  → io/escribir_excel.py
```

## Entrada

DataFrames con nombres = claves de `LECTURAS` en `python/io/leer_h2.py`.

SINADA: `DERIV_2020` ← `STG_GS1_SINADA_DERIV`, `DERIV_2021` ← `STG_GS2_SINADA_DERIV`.

## Salida obligatoria

| Nombre | Descripción |
|---|---|
| `RESULTADO` | 26 campos de Derivaciones + `ANIO`. Va a Oracle `RP_SINADA_DENUNCIAS_DERIVACIONES` y a Excel. |

Salidas opcionales reconocidas por main: prefijos `INT_`, `QA_`, `PROF_`, `DF_`.

## Reglas

- Un solo `.py` en `logica/`.
- Sin conexiones ni drivers en `logica/` (I/O en `python/io/`).
- `pandas` inyectado como `pd`.

Plantilla: `python/plantilla_logica.py`.
