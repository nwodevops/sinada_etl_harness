# Sesión activa

| Campo | Valor |
|---|---|
| ID | fase-5-catalogos |
| Criterio | Cuatro tablas `RP_SINADA_*` con `COUNT(*)` en el log de init |

## Hecho

Directorio SEFA, REGISTROS, UBIGEO y Feriados en tablas Oracle aparte de `RP_SINADA_DENUNCIAS_DERIVACIONES`.

Evidencia: [`impl_fase-5-catalogos.md`](impl_fase-5-catalogos.md).

## Windows pendiente de corrida

`init.bat remote` en el otro equipo. Linux no lo ejecuta.
