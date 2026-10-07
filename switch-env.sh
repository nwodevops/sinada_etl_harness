#!/usr/bin/env bash
# Copia environments/<env>.json -> project-config.json y sobrepone DB_ORA_DW_*
# desde docs/credenciales/<env>.txt. No copia SysPassword. No escribe secretos en stdout.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
ENV="${1:-local}"
SRC="$ROOT/environments/${ENV}.json"
DST="$ROOT/project-config.json"
CRED="$ROOT/docs/credenciales/${ENV}.txt"
if [[ ! -f "$SRC" ]]; then
  echo "No existe: $SRC" >&2
  exit 1
fi
python3 - "$SRC" "$DST" "$CRED" "$ENV" <<'PY'
import json
import sys
from pathlib import Path

src, dst, cred_path, env_name = sys.argv[1:]
data = json.loads(Path(src).read_text(encoding="utf-8"))
variables = data.get("variables") or data.get("config", {}).get("variables") or []
variables = [dict(item) for item in variables]

KEYMAP = {
    "host": "DB_ORA_DW_HOST",
    "port": "DB_ORA_DW_PORT",
    "service": "DB_ORA_DW_DATABASE",
    "user": "DB_ORA_DW_USERNAME",
    "password": "DB_ORA_DW_PASSWORD",
    "schema": "DB_ORA_DW_SCHEMA",
}


def parse_cred(path: Path) -> dict[str, str]:
    found: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if key == "syspassword" or key not in KEYMAP or not value:
            continue
        found[key] = value
    return found


def upsert(name: str, value: str, description: str) -> None:
    for item in variables:
        if item.get("name") == name:
            item["value"] = value
            return
    variables.append({"name": name, "value": value, "description": description})


cred_file = Path(cred_path)
if not cred_file.is_file():
    print(
        f"AVISO: no existe {cred_file}; DB_ORA_DW_* quedan como en {src}",
        file=sys.stderr,
    )
else:
    cred = parse_cred(cred_file)
    if "schema" not in cred and cred.get("user"):
        cred["schema"] = cred["user"].upper()
    for key, var_name in KEYMAP.items():
        if cred.get(key):
            upsert(var_name, cred[key], f"Oracle DW desde docs/credenciales/{env_name}.txt")
    host, port, service = cred.get("host"), cred.get("port"), cred.get("service")
    if host and port and service:
        upsert(
            "DB_ORA_DW_URL",
            f"jdbc:oracle:thin:@//{host}:{port}/{service}",
            f"Oracle DW desde docs/credenciales/{env_name}.txt",
        )
    schema = cred.get("schema") or ""
    print(f"OK: overlay DB_ORA_DW_* desde {cred_file} (schema={schema})")

out = {
    "metadataBaseFolder": "${PROJECT_HOME}/metadata",
    "unitTestsBasePath": "${PROJECT_HOME}",
    "dataSetsCsvFolder": "${PROJECT_HOME}/datasets",
    "enforcingExecutionInHome": True,
    "parentProjectName": "default",
    "config": {"variables": variables},
}
Path(dst).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"OK: {src} -> {dst}")
PY
