# Bitácora harness (append-only)

---

## Plantilla

Al cerrar una feature, append aquí: fecha, id, resumen, evidencia (`progress/impl_<id>.md`).

---

## 2026-10-05 — fase-1-entorno, fase-2-fuentes-stg, fase-3-logica, fase-4-oracle

Sheets Derivaciones 2020 y 2021 homologadas a 26 campos + `ANIO` y cargadas en `RP_SINADA_DENUNCIAS_DERIVACIONES`. Evidencia: `progress/impl_fase-4-oracle.md`.

---

## 2026-10-07 — fase-5-catalogos

Directorio SEFA, REGISTROS, UBIGEO y Feriados en `RP_SINADA_DIRECTORIO_SEFA`, `RP_SINADA_REGISTROS`, `RP_SINADA_UBIGEO` y `RP_SINADA_FERIADOS`. `./init.sh` cerró en `HARNESS OK`. Evidencia: `progress/impl_fase-5-catalogos.md`.

---

## 2026-10-07 — cierre Linux y Windows

`./init.sh` en Linux y la corrida Windows (`init.bat remote` / `wf_main_windows`) terminaron bien. Ninguna feature `in_progress`. Evidencia: `progress/impl_fase-5-catalogos.md`.

---

## 2026-10-13 — fase-6-oefa

Diez pestañas de `TABLAS SINADA_OEFA v11` en `RP_SINADA_OEFA_*`. `./init.sh` cerró en `HARNESS OK`. Evidencia: `progress/impl_fase-6-oefa.md`.

---

## 2026-10-13 — fase-7-tipos

Los 60 campos del listado quedaron `DATE` o `NUMBER`. El resto sigue `VARCHAR2`. `./init.sh` cerró en `HARNESS OK`. Evidencia: `progress/impl_fase-7-tipos.md`.
