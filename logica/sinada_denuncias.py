# Homologa Derivaciones 2019, 2020, 2021 y la matriz a una sola tabla.
# Sin conexiones: los DataFrames llegan de python/io/leer_h2.py.

import re

from sinada_campos import (
    ALIAS_MATRIZ,
    CAMPOS,
    CAMPOS_DIRECTORIO,
    CAMPOS_FERIADOS,
    CAMPOS_REGISTROS,
    CAMPOS_UBIGEO,
    COLS_DIRECTORIO,
    COLS_FERIADOS,
    COLS_REGISTROS,
    COLS_UBIGEO,
    EXTRAS,
    ORACLE_COLUMNS,
)

_IDENT_RE = re.compile(r"[^A-Za-z0-9_]")
_ANIO_CODIGO = re.compile(r"-(20\d{2})$")
_EXTRA_NOMBRES = [nombre for _header, nombre in EXTRAS]


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


def _anio_de_codigo(codigo):
    if _vacio(codigo):
        return None
    hallado = _ANIO_CODIGO.search(str(codigo).strip())
    return hallado.group(1) if hallado else None


def _proyectar(df, campos, etiqueta: str, *, extras: bool = True):
    if df is None or len(getattr(df, "columns", [])) == 0:
        raise ValueError(f"STG {etiqueta} vacía: no hay columnas")
    columnas = {str(col).upper(): col for col in df.columns}
    rename = {}
    faltan = []
    for header, ora in campos:
        h2_name = _sanitize(header)
        src = columnas.get(h2_name)
        if src is None:
            faltan.append(f"{header} -> {h2_name}")
        else:
            rename[src] = ora
    if faltan:
        raise ValueError(f"STG {etiqueta} sin columnas: {', '.join(faltan)}")
    # Serie por header. Un rename del marco entero duplica EFA: el sheet ya trae esa columna.
    data = {ora: df[src].map(_texto) for src, ora in rename.items()}
    if extras:
        for col in _EXTRA_NOMBRES:
            if col not in data:
                data[col] = None
    return pd.DataFrame(data)


def _catalogo(df, campos, etiqueta: str, columnas: list[str]):
    out = _proyectar(df, campos, etiqueta, extras=False)
    vacias = out[columnas].apply(lambda fila: all(_vacio(valor) for valor in fila), axis=1)
    return out.loc[~vacias, columnas].copy()


def _cerrar(out, anio_fijo):
    es_diccionario = out["CODIGO_SINADA"].map(
        lambda valor: isinstance(valor, str) and valor.strip().upper() == "COD_SINADA"
    )
    out = out.loc[~es_diccionario].copy()
    negocio = [col for col in ORACLE_COLUMNS if col != "ANIO"]
    vacias = out[negocio].apply(lambda fila: all(_vacio(valor) for valor in fila), axis=1)
    out = out.loc[~vacias].copy()
    if anio_fijo is None:
        out["ANIO"] = out["CODIGO_SINADA"].map(_anio_de_codigo)
    else:
        out["ANIO"] = anio_fijo
    return out[ORACLE_COLUMNS]


RESULTADO = pd.concat(
    [
        _cerrar(_proyectar(DERIV_2019, CAMPOS, "2019"), "2019"),
        _cerrar(_proyectar(DERIV_2020, CAMPOS, "2020"), "2020"),
        _cerrar(_proyectar(DERIV_2021, CAMPOS, "2021"), "2021"),
        _cerrar(_proyectar(DERIV_MATRIZ, ALIAS_MATRIZ, "MATRIZ"), None),
    ],
    ignore_index=True,
)

DIRECTORIO = _catalogo(DIR_SEFA, CAMPOS_DIRECTORIO, "DIRECTORIO", COLS_DIRECTORIO)
REGISTROS = _catalogo(CIF_REGISTROS, CAMPOS_REGISTROS, "REGISTROS", COLS_REGISTROS)
UBIGEO = _catalogo(CIF_UBIGEO, CAMPOS_UBIGEO, "UBIGEO", COLS_UBIGEO)
FERIADOS = _catalogo(FERIADOS_SRC, CAMPOS_FERIADOS, "FERIADOS", COLS_FERIADOS)
