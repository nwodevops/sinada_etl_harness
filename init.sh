#!/usr/bin/env bash
# Corrida Linux: credenciales local, H2, Sheets Derivaciones, Oracle DW.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
mkdir -p logs
LOGFILE="$ROOT/logs/init_$(date +%Y%m%d).log"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

fail() { echo -e "${RED}FAIL:${NC} $*" | tee -a "$LOGFILE" >&2; exit 1; }
step() { echo -e "${GREEN}==>${NC} $*" | tee -a "$LOGFILE"; }

PY=python3
[ -x .venv/bin/python ] && PY=.venv/bin/python

run_step() {
  set +e
  "$@" 2>&1 | tee -a "$LOGFILE"
  local rc=${PIPESTATUS[0]}
  set -e
  return "$rc"
}

step "Validando feature_list.json"
"$PY" - <<'PY' 2>&1 | tee -a "$LOGFILE"
import json, sys
from pathlib import Path
data = json.loads(Path("feature_list.json").read_text(encoding="utf-8"))
active = [f for f in data.get("features", []) if f.get("status") == "in_progress"]
if len(active) > 1:
    sys.exit(f"más de una in_progress: {', '.join(f['id'] for f in active)}")
print(f"features: {len(data.get('features', []))}, in_progress: {len(active)}")
PY

step "Prerrequisitos"
command -v java >/dev/null 2>&1 || fail "java no está en PATH"
[ -f h2/lib/h2-2.4.240.jar ] || fail "jar H2 no encontrado"
if [ ! -x .venv/bin/python ]; then
  fail "venv ausente o roto. Desde el repo padre: ./scripts/nuevo_etl.sh lo crea. A mano: python3 -m venv .venv && .venv/bin/python -m pip install -r python/requirements.txt"
fi
"$PY" -c "import yaml, pandas, jaydebeapi, gspread, oracledb" 2>/dev/null \
  || fail "el .venv no tiene dependencias. .venv/bin/python -m pip install -r python/requirements.txt"
[ -f client_secret.json ] || fail "falta client_secret.json (service account Google, gitignored)"

step "Entorno local"
./switch-env.sh local 2>&1 | tee -a "$LOGFILE"

step "Reset H2 + DDL"
run_step ./h2/scripts/reset_and_create.sh || fail "reset H2"

step "Python create STG"
run_step "$PY" python/create_stg.py || fail "python/create_stg.py"

step "Cargar Sheets a H2"
run_step "$PY" python/io/cargar_stg_sheets.py || fail "python/io/cargar_stg_sheets.py"

step "Python main (logica + Oracle + Excel)"
run_step "$PY" python/main.py || fail "python/main.py"

step "Comprobando salidas"
grep -q "STG_GS3_SINADA_DERIV: " "$LOGFILE" || fail "no hay conteo STG_GS3_SINADA_DERIV"
grep -q "STG_GS1_SINADA_DERIV: " "$LOGFILE" || fail "no hay conteo STG_GS1_SINADA_DERIV"
grep -q "STG_GS2_SINADA_DERIV: " "$LOGFILE" || fail "no hay conteo STG_GS2_SINADA_DERIV"
grep -q "STG_GS4_SINADA_MATRIZ: " "$LOGFILE" || fail "no hay conteo STG_GS4_SINADA_MATRIZ"
grep -q "STG_GS5_DIRECTORIO: " "$LOGFILE" || fail "no hay conteo STG_GS5_DIRECTORIO"
grep -q "STG_GS6_REGISTROS: " "$LOGFILE" || fail "no hay conteo STG_GS6_REGISTROS"
grep -q "STG_GS7_UBIGEO: " "$LOGFILE" || fail "no hay conteo STG_GS7_UBIGEO"
grep -q "STG_GS8_FERIADOS: " "$LOGFILE" || fail "no hay conteo STG_GS8_FERIADOS"
grep -q "STG_GS9_OEFA_REGISTROS: " "$LOGFILE" || fail "no hay conteo STG_GS9_OEFA_REGISTROS"
grep -q "STG_GS10_OEFA_SEGUIMIENTO: " "$LOGFILE" || fail "no hay conteo STG_GS10_OEFA_SEGUIMIENTO"
grep -q "STG_GS11_OEFA_ASIGNACIONES: " "$LOGFILE" || fail "no hay conteo STG_GS11_OEFA_ASIGNACIONES"
grep -q "STG_GS12_OEFA_EVALUACION: " "$LOGFILE" || fail "no hay conteo STG_GS12_OEFA_EVALUACION"
grep -q "STG_GS13_OEFA_VALIDACION: " "$LOGFILE" || fail "no hay conteo STG_GS13_OEFA_VALIDACION"
grep -q "STG_GS14_OEFA_DOC_COMUNIC: " "$LOGFILE" || fail "no hay conteo STG_GS14_OEFA_DOC_COMUNIC"
grep -q "STG_GS15_OEFA_DOC_DERIV: " "$LOGFILE" || fail "no hay conteo STG_GS15_OEFA_DOC_DERIV"
grep -q "STG_GS16_OEFA_VAL_RPTA: " "$LOGFILE" || fail "no hay conteo STG_GS16_OEFA_VAL_RPTA"
grep -q "STG_GS17_OEFA_DOC_REI: " "$LOGFILE" || fail "no hay conteo STG_GS17_OEFA_DOC_REI"
grep -q "STG_GS18_OEFA_DOC_OCI: " "$LOGFILE" || fail "no hay conteo STG_GS18_OEFA_DOC_OCI"
if grep -E 'STG_GS[123]_SINADA_DERIV: 0 filas|STG_GS4_SINADA_MATRIZ: 0 filas|STG_GS5_DIRECTORIO: 0 filas|STG_GS6_REGISTROS: 0 filas|STG_GS7_UBIGEO: 0 filas|STG_GS8_FERIADOS: 0 filas|STG_GS9_OEFA_REGISTROS: 0 filas|STG_GS1[0-8]_OEFA_[A-Z_]+: 0 filas' "$LOGFILE"; then
  fail "una STG de Sheets quedó en 0 filas"
fi
grep -q "Salida RESULTADO" "$LOGFILE" || fail "no hay Salida RESULTADO en el log"
grep -q "Excel:" "$LOGFILE" || fail "no se escribió Excel"
grep -q "Oracle RP_SINADA_DENUNCIAS_DERIVACIONES: " "$LOGFILE" || fail "no hay COUNT(*) de denuncias"
grep -q "Oracle RP_SINADA_DIRECTORIO_SEFA: " "$LOGFILE" || fail "no hay COUNT(*) de directorio"
grep -q "Oracle RP_SINADA_REGISTROS: " "$LOGFILE" || fail "no hay COUNT(*) de registros"
grep -q "Oracle RP_SINADA_UBIGEO: " "$LOGFILE" || fail "no hay COUNT(*) de ubigeo"
grep -q "Oracle RP_SINADA_FERIADOS: " "$LOGFILE" || fail "no hay COUNT(*) de feriados"
grep -q "Oracle RP_SINADA_OEFA_REGISTROS: " "$LOGFILE" || fail "no hay COUNT(*) de oefa registros"
grep -q "Oracle RP_SINADA_OEFA_SEGUIMIENTO: " "$LOGFILE" || fail "no hay COUNT(*) de oefa seguimiento"
grep -q "Oracle RP_SINADA_OEFA_ASIGNACIONES: " "$LOGFILE" || fail "no hay COUNT(*) de oefa asignaciones"
grep -q "Oracle RP_SINADA_OEFA_EVALUACION: " "$LOGFILE" || fail "no hay COUNT(*) de oefa evaluacion"
grep -q "Oracle RP_SINADA_OEFA_VALIDACION: " "$LOGFILE" || fail "no hay COUNT(*) de oefa validacion"
grep -q "Oracle RP_SINADA_OEFA_DOC_COMUNIC: " "$LOGFILE" || fail "no hay COUNT(*) de oefa doc comunic"
grep -q "Oracle RP_SINADA_OEFA_DOC_DERIV: " "$LOGFILE" || fail "no hay COUNT(*) de oefa doc deriv"
grep -q "Oracle RP_SINADA_OEFA_VAL_RPTA: " "$LOGFILE" || fail "no hay COUNT(*) de oefa val rpta"
grep -q "Oracle RP_SINADA_OEFA_DOC_REI: " "$LOGFILE" || fail "no hay COUNT(*) de oefa doc rei"
grep -q "Oracle RP_SINADA_OEFA_DOC_OCI: " "$LOGFILE" || fail "no hay COUNT(*) de oefa doc oci"
if grep -q '\${[A-Za-z0-9_]\+}' "$LOGFILE"; then
  fail "log contiene variables Hop sin resolver"
fi

echo "" | tee -a "$LOGFILE"
echo -e "${GREEN}HARNESS OK${NC} — ver CHECKPOINTS.md" | tee -a "$LOGFILE"
exit 0
