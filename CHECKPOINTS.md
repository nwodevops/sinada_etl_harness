# CHECKPOINTS — arquetipo mínimo

Criterios para marcar features `done` en [`feature_list.json`](feature_list.json).  
Verificación: [`./init.sh`](init.sh).

---

## Global

- [ ] `./init.sh` termina con **`HARNESS OK`**.
- [ ] Sin passwords reales en `project-config.json` / `environments/`.
- [ ] Log sin literales `${VAR}`.
- [ ] Un solo `.py` en `logica/`.
- [ ] Máximo **una** feature `in_progress`.

---

## Fase 1 — Entorno {#fase-1}

- [ ] H2 levanta en puerto 9092 (`reset_and_create.sh`).
- [ ] `python/create_stg.py` OK (puede ser no-op con `sources: []`).
- [ ] `python/main.py` OK con `logica/demo.py`.
- [ ] `wf_main.hwf` ejecutable en Hop GUI.

---

## Fase 2 — Fuentes STG {#fase-2}

- [ ] Al menos una fuente en `inputs.yaml`.
- [ ] Tabla `STG_*` creada en H2.
- [ ] Carga Sheets en `python/io/cargar_stg_sheets.py`, cableada en `wf_main.hwf` (donde iría `pl_stage_*`).
- [ ] Conteos `STG_GS1_SINADA_DERIV` y `STG_GS2_SINADA_DERIV` > 0 en el log.

Ver skill `hop-python-etl` e [`inputs.example.yaml`](.agents/skills/hop-python-etl/inputs.example.yaml).
Sheets no pasan por `GoogleSheetsInput`: el paso SHELL usa el mismo `client_secret.json` que la introspección.

---

## Fase 3 — Lógica {#fase-3}

- [ ] Claves STG en `python/io/leer_h2.py`.
- [ ] `logica/<tu_logica>.py` produce `RESULTADO` con filas > 0.
- [ ] `output/resultado.xlsx` generado (si se usa salida Excel).

Contrato: [`python/CONTRATO.md`](python/CONTRATO.md).

---

## Fase 4 — Oracle {#fase-4}

- [ ] `python/io/cargar_dw.py` hace DDL si falta, luego `TRUNCATE` + `INSERT`.
- [ ] Tabla `RP_SINADA_DENUNCIAS_DERIVACIONES` en el esquema `DB_ORA_DW_SCHEMA` (sin esquema literal en el SQL).
- [ ] El log trae `COUNT(*)` de Oracle y coincide con `RESULTADO`.

## Fuera de alcance

- Fases Kimball / indicadores → no vienen en esta plantilla.
