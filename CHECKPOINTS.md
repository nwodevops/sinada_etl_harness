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

## Cierre 2026-10-07

- [x] Linux: `./init.sh` → `HARNESS OK` (`logs/init_20261007.log`).
- [x] Windows: corrida completa en `wf_main_windows` / `init.bat remote`. El venv se crea en el equipo (no va en git) y lleva `python/requirements.txt`.
- [x] Ninguna feature `in_progress`.

---

## Fase 1 — Entorno {#fase-1}

- [x] H2 levanta en puerto 9092 (`reset_and_create.sh` / `reset_and_create.bat`).
- [x] `python/create_stg.py` crea las STG de `inputs.yaml`.
- [x] `python/main.py` corre `logica/sinada_denuncias.py`.
- [x] `wf_main.hwf` (Linux) y `wf_main_windows.hwf` (Windows).

---

## Fase 2 — Fuentes STG {#fase-2}

- [x] Ocho fuentes Sheets en `inputs.yaml`.
- [x] Carga en `python/io/cargar_stg_sheets.py`, cableada en `wf_main.hwf` y en `scripts/step_cargar_sheets.bat`.
- [x] Conteos > 0: `STG_GS3_SINADA_DERIV`, `STG_GS1_SINADA_DERIV`, `STG_GS2_SINADA_DERIV`, `STG_GS4_SINADA_MATRIZ`, `STG_GS5_DIRECTORIO`, `STG_GS6_REGISTROS`, `STG_GS7_UBIGEO`, `STG_GS8_FERIADOS`.

Sheets no pasan por `GoogleSheetsInput`. El paso SHELL usa `client_secret.json`.

---

## Fase 3 — Lógica {#fase-3}

- [x] Claves STG en `python/io/leer_h2.py`.
- [x] `logica/sinada_denuncias.py` deja `RESULTADO` con filas > 0.
- [x] `output/resultado.xlsx` solo con `RESULTADO`.

Contrato: [`python/CONTRATO.md`](python/CONTRATO.md).

---

## Fase 4 — Oracle denuncias {#fase-4}

- [x] `python/io/cargar_dw.py`: `DROP` + `CREATE` si el esquema no coincide; si coincide, `TRUNCATE` + `INSERT`.
- [x] `RP_SINADA_DENUNCIAS_DERIVACIONES` en el esquema `DB_ORA_DW_SCHEMA` (sin esquema literal en el SQL).
- [x] El log trae `COUNT(*)` y coincide con `RESULTADO`.

---

## Fase 5 — Catálogos {#fase-5}

- [x] `RP_SINADA_DIRECTORIO_SEFA`, `RP_SINADA_REGISTROS`, `RP_SINADA_UBIGEO`, `RP_SINADA_FERIADOS`.
- [x] Cada `COUNT(*)` en el log de `init.sh` e `init.bat`. Sin `ANIO`.

---

## Fase 6 — SINADA OEFA {#fase-6}

- [x] Diez pestañas de `TABLAS SINADA_OEFA v11` en `RP_SINADA_OEFA_*`. Sin `ANIO` y sin campo calculado.
- [x] `./init.sh` → `HARNESS OK` (`logs/init_20261013.log`). Cada `COUNT(*)` en `init.sh` e `init.bat`.

---

## Fase 7 — Tipos {#fase-7}

- [x] Los 60 campos de `input/req_user/DETALLE CAMPOS.xlsx` salen `DATE` o `NUMBER`. El resto sigue `VARCHAR2`.
- [x] `./init.sh` → `HARNESS OK` el 2026-10-13, con `DROP` por esquema distinto en las tablas tocadas.

## Fuera de alcance

- Fases Kimball / indicadores.
