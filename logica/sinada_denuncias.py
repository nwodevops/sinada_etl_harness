# Homologa STG_GS1 (2020) y STG_GS2 (2021) a los 26 campos de Derivaciones.
# Sin conexiones: los DataFrames llegan de python/io/leer_h2.py.

import re

from sinada_campos import CAMPOS

_IDENT_RE = re.compile(r"[^A-Za-z0-9_]")


def _sanitize(name: str) -> str:
    """Igual que introspect.h2_ddl.sanitize_ident, sin el sufijo de colisión."""
    raw = "" if name is None else str(name).strip()
    cleaned = _IDENT_RE.sub("_", raw)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    if not cleaned:
        cleaned = "COL"
    if cleaned[0].isdigit():
        cleaned = "C_" + cleaned
    return cleaned.upper()


def _vacio(val) -> bool:
    if val is None:
        return True
    try:
        if pd.isna(val):
            return True
    except TypeError:
        pass
    return str(val).strip() == ""


def _texto(val):
    if _vacio(val):
        return None
    return str(val).strip()


def _proyectar(df, anio: str):
    if df is None or len(getattr(df, "columns", [])) == 0:
        raise ValueError(f"STG {anio} vacía: no hay columnas")
    columnas = {str(col).upper(): col for col in df.columns}
    rename = {}
    faltan = []
    for header, ora in CAMPOS:
        h2_name = _sanitize(header)
        src = columnas.get(h2_name)
        if src is None:
            faltan.append(f"{header} -> {h2_name}")
        else:
            rename[src] = ora
    if faltan:
        raise ValueError(f"STG {anio} sin columnas: {', '.join(faltan)}")
    orden = [ora for _header, ora in CAMPOS]
    out = df.rename(columns=rename)[orden].copy()
    for col in orden:
        out[col] = out[col].map(_texto)
    vacias = out.apply(lambda row: all(_vacio(v) for v in row), axis=1)
    out = out.loc[~vacias].copy()
    out["ANIO"] = anio
    return out


RESULTADO = pd.concat(
    [_proyectar(DERIV_2020, "2020"), _proyectar(DERIV_2021, "2021")],
    ignore_index=True,
)
