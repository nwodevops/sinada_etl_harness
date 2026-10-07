"""Campos destino de RP_SINADA_DENUNCIAS_DERIVACIONES. Sin I/O.

El header canónico es el de input/notas.txt. En 2020 falta el espacio antes
de '[' en la fecha de notificación del documento; sanitize_ident los iguala.
"""

from __future__ import annotations

TABLE = "RP_SINADA_DENUNCIAS_DERIVACIONES"

# (header de la hoja Derivaciones 2019/2020/2021, columna Oracle de notas.txt)
CAMPOS: list[tuple[str, str]] = [
    ("Código Sinada", "CODIGO_SINADA"),
    ("Acciones adoptadas", "ACCION_ADOPTADA"),
    ("HT derivación", "HT"),
    ("Efa competente", "EFA"),
    ("Tipo de destinatario [Casilla automática]", "TIPO_EFA"),
    ("Plazo otorgado para la respuesta [Días hábiles]", "PLAZO"),
    ("Días transcurridos desde la notificación [Casilla automática]", "DIAS_TRANSCURRIDOS"),
    ("Seguimiento a la respuesta al documento emitido [Casilla automática]", "SEGUIMIENTO_RPTA"),
    ("N° del documento emitido", "NRO_DOC"),
    ("Fecha de firma del documento", "FECHA_FIRMA"),
    ("Fecha de notificación del documento [Ver cargo]", "FECHA_NOTIFICACION"),
    ("HT de respuesta", "HT_RESPUESTA"),
    ("Fecha de recepción de la primera respuesta", "FECHA_RESPUESTA"),
    ("HT de respuesta post cierre", "HT_RESPUESTA_POSTCIERRE"),
    ("Fecha de recepción del documento de respuesta después del cierre", "FECHA_RESPUESTA_POSTCIERRE"),
    ("HT reiterativo", "HT_REITERATIVO"),
    ("N° del documento reiterativo", "NRO_REITERATIVO"),
    ("Plazo de respuesta al reiterativo [Días hábiles]", "PLAZO_REITERATIVO"),
    ("Fecha de firma del documento reiterativo", "FECHA_FIRMA_REITERATIVO"),
    ("Fecha de notificación del reiterativo [Ver cargo]", "FECHA_NOTIFICACION_REITERATIVO"),
    ("Días transcurridos desde la notificación reiterativo [Casilla automática]", "DIAS_TRANSCURRIDOS_REITERATIVO"),
    ("Seguimiento a la respuesta al reiterativo [Casilla automática]", "SEGUIMIENTO_RPTA_REITERATIVO"),
    ("N° del oficio con el que se envía el informe a OCI", "NRO_OCI"),
    ("Fecha de firma del informe a OCI", "FECHA_FIRMA_OCI"),
    ("Fecha de notificación del doc con el que se envía informe a OCI", "FECHA_NOTIFICACION_OCI"),
    ("Calificación de la respuesta", "CALIFICACION_RPTA"),
    ("Supuesto que concluye el seguimiento", "SUPUESTO_CIERRE"),
]

# Solo la matriz. 2019/2020/2021 dejan estas columnas en nulo.
EXTRAS: list[tuple[str, str]] = [
    ("FECHA ENVIO PROYECTO REITERATIVO", "FECHA_ENVIO_PROYEC_REITERATIVO"),
    (
        "DIAS HABILES TRANSCURRIDOS DESDE VENCIMIENTO DE DERIVACIÓN/SOLICITUD FINAL HASTA  OCI",
        "DIAS_VENCIMIENTO_PARAOCI",
    ),
    (
        "TAREA A REALIZAR RESPECTO VENCIMIENTO DE DERIVACIÓN O SOLICITUD FINAL",
        "TAREA_OCI",
    ),
]

# Header real de la matriz → el mismo código Oracle de notas.txt.
ALIAS_MATRIZ: list[tuple[str, str]] = [
    ("CODIGO SINADA", "CODIGO_SINADA"),
    ("ACCIONES ADOPTADAS", "ACCION_ADOPTADA"),
    ("HT DERIVACION", "HT"),
    ("EFA COMPETENTE", "EFA"),
    ("TIPO DESTINATARIO", "TIPO_EFA"),
    ("PLAZO OTORGADO EN DIAS HABILES", "PLAZO"),
    ("DIAS HABILES TRANSCURRIDOS DESDE NOTIFICACION", "DIAS_TRANSCURRIDOS"),
    ("SEGUIMIENTO A LA RESPUESTA DEL DOC EMITIDO", "SEGUIMIENTO_RPTA"),
    ("NRO DOCUMENTO EMITIDO", "NRO_DOC"),
    ("FECHA FIRMA DOCUMENTO", "FECHA_FIRMA"),
    ("FECHA DE NOTIFICACION", "FECHA_NOTIFICACION"),
    ("HT DE RESPUESTA", "HT_RESPUESTA"),
    ("FECHA DE RECEPCION DE LA PRIMERA RESPUESTA", "FECHA_RESPUESTA"),
    ("HT DE RESPUESTA POST CIERRE", "HT_RESPUESTA_POSTCIERRE"),
    (
        "FECHA DE RECEPCION DEL DOCUMENTO DE RESPUESTA DESPUES DEL CIERRE",
        "FECHA_RESPUESTA_POSTCIERRE",
    ),
    ("HT REITERATIVO", "HT_REITERATIVO"),
    ("NRO DEL DOCUMENTO REITERATIVO", "NRO_REITERATIVO"),
    ("PLAZO DE RPTA AL REITERATIVO", "PLAZO_REITERATIVO"),
    ("FECHA DE FIRMA DEL DOCUMENTO REITERATIVO", "FECHA_FIRMA_REITERATIVO"),
    ("FECHA DE NOTIFICACION DEL REITERATIVO", "FECHA_NOTIFICACION_REITERATIVO"),
    (
        "DIAS HABILES TRANSCURRIDOS DESDE NOTIFICACION REITERATIVO",
        "DIAS_TRANSCURRIDOS_REITERATIVO",
    ),
    ("SEGUIMIENTO A LA RESPUESTA DEL REITERATIVO", "SEGUIMIENTO_RPTA_REITERATIVO"),
    ("NRO DEL OFICIO AL OCI", "NRO_OCI"),
    ("FECHA FIRMA DEL OFICIO AL OCI", "FECHA_FIRMA_OCI"),
    ("FECHA NOTIFICACION DEL OFICIO AL OCI", "FECHA_NOTIFICACION_OCI"),
    ("CALIFICACION DE LA RESPUESTA", "CALIFICACION_RPTA"),
    ("SUPUESTO QUE CONCLUYE EL SEGUIMIENTO", "SUPUESTO_CIERRE"),
    *EXTRAS,
]

# Orden de la matriz: es el superconjunto. Las tres extras quedan en medio, como en notas.txt.
ORACLE_COLUMNS: list[str] = [
    "CODIGO_SINADA",
    "ACCION_ADOPTADA",
    "HT",
    "EFA",
    "TIPO_EFA",
    "PLAZO",
    "DIAS_TRANSCURRIDOS",
    "SEGUIMIENTO_RPTA",
    "NRO_DOC",
    "FECHA_FIRMA",
    "FECHA_NOTIFICACION",
    "HT_RESPUESTA",
    "FECHA_RESPUESTA",
    "HT_RESPUESTA_POSTCIERRE",
    "FECHA_RESPUESTA_POSTCIERRE",
    "FECHA_ENVIO_PROYEC_REITERATIVO",
    "DIAS_VENCIMIENTO_PARAOCI",
    "TAREA_OCI",
    "HT_REITERATIVO",
    "NRO_REITERATIVO",
    "PLAZO_REITERATIVO",
    "FECHA_FIRMA_REITERATIVO",
    "FECHA_NOTIFICACION_REITERATIVO",
    "DIAS_TRANSCURRIDOS_REITERATIVO",
    "SEGUIMIENTO_RPTA_REITERATIVO",
    "NRO_OCI",
    "FECHA_FIRMA_OCI",
    "FECHA_NOTIFICACION_OCI",
    "CALIFICACION_RPTA",
    "SUPUESTO_CIERRE",
    "ANIO",
]

CAMPOS_DIRECTORIO: list[tuple[str, str]] = [
    ("Entidad u oficina", "EFA"),
    ("Tipo de entidad u oficina", "TIPO_EFA"),
    ("Tipo de documento que pertenece", "TIPO_DOC"),
]
COLS_DIRECTORIO = [nombre for _header, nombre in CAMPOS_DIRECTORIO]

CAMPOS_REGISTROS: list[tuple[str, str]] = [
    ("CODIGO_SINADA", "CODIGO_SINADA"),
    ("FECHA_INGRESO", "FECHA_INGRESO"),
    ("FECHA_REGISTRO", "FECHA_REGISTRO"),
]
COLS_REGISTROS = [nombre for _header, nombre in CAMPOS_REGISTROS]

CAMPOS_UBIGEO: list[tuple[str, str]] = [
    ("CODIGO_SINADA", "CODIGO_SINADA"),
    ("DEPARTAMENTO", "DEPARTAMENTO"),
    ("PROVINCIA", "PROVINCIA"),
    ("DISTRITO", "DISTRITO"),
    ("NU_COORDENADA_X", "NU_COORDENADA_X"),
    ("NU_COORDENADA_Y", "NU_COORDENADA_Y"),
]
COLS_UBIGEO = [nombre for _header, nombre in CAMPOS_UBIGEO]

CAMPOS_FERIADOS: list[tuple[str, str]] = [
    ("DP", "FERIADO"),
]
COLS_FERIADOS = [nombre for _header, nombre in CAMPOS_FERIADOS]

# (nombre del DataFrame en logica/, tabla Oracle, columnas)
TABLAS: list[tuple[str, str, list[str]]] = [
    ("RESULTADO", TABLE, ORACLE_COLUMNS),
    ("DIRECTORIO", "RP_SINADA_DIRECTORIO_SEFA", COLS_DIRECTORIO),
    ("REGISTROS", "RP_SINADA_REGISTROS", COLS_REGISTROS),
    ("UBIGEO", "RP_SINADA_UBIGEO", COLS_UBIGEO),
    ("FERIADOS", "RP_SINADA_FERIADOS", COLS_FERIADOS),
]
