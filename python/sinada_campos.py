"""Campos destino de RP_SINADA_DENUNCIAS_DERIVACIONES. Sin I/O.

El header canónico es el de input/notas.txt. En 2020 falta el espacio antes
de '[' en la fecha de notificación del documento; sanitize_ident los iguala.
"""

from __future__ import annotations

TABLE = "RP_SINADA_DENUNCIAS_DERIVACIONES"

# (header de la hoja Derivaciones, columna Oracle)
CAMPOS: list[tuple[str, str]] = [
    ("Código Sinada", "CODIGO_SINADA"),
    ("Acciones adoptadas", "ACCIONES_ADOPTADAS"),
    ("HT derivación", "HT_DERIVACION"),
    ("Efa competente", "EFA_COMPETENTE"),
    ("Tipo de destinatario [Casilla automática]", "TIPO_DESTINATARIO"),
    ("Plazo otorgado para la respuesta [Días hábiles]", "PLAZO_RESPUESTA_DIAS"),
    ("Días transcurridos desde la notificación [Casilla automática]", "DIAS_DESDE_NOTIFICACION"),
    ("Seguimiento a la respuesta al documento emitido [Casilla automática]", "SEGUIMIENTO_RESPUESTA"),
    ("N° del documento emitido", "NRO_DOCUMENTO"),
    ("Fecha de firma del documento", "FECHA_FIRMA_DOCUMENTO"),
    ("Fecha de notificación del documento [Ver cargo]", "FECHA_NOTIFICACION_DOCUMENTO"),
    ("HT de respuesta", "HT_RESPUESTA"),
    ("Fecha de recepción de la primera respuesta", "FECHA_RECEPCION_PRIMERA_RESPUESTA"),
    ("HT de respuesta post cierre", "HT_RESPUESTA_POST_CIERRE"),
    ("Fecha de recepción del documento de respuesta después del cierre", "FECHA_RECEPCION_POST_CIERRE"),
    ("HT reiterativo", "HT_REITERATIVO"),
    ("N° del documento reiterativo", "NRO_DOCUMENTO_REITERATIVO"),
    ("Plazo de respuesta al reiterativo [Días hábiles]", "PLAZO_REITERATIVO_DIAS"),
    ("Fecha de firma del documento reiterativo", "FECHA_FIRMA_REITERATIVO"),
    ("Fecha de notificación del reiterativo [Ver cargo]", "FECHA_NOTIFICACION_REITERATIVO"),
    ("Días transcurridos desde la notificación reiterativo [Casilla automática]", "DIAS_DESDE_NOTIFICACION_REITERATIVO"),
    ("Seguimiento a la respuesta al reiterativo [Casilla automática]", "SEGUIMIENTO_REITERATIVO"),
    ("N° del oficio con el que se envía el informe a OCI", "NRO_OFICIO_OCI"),
    ("Fecha de firma del informe a OCI", "FECHA_FIRMA_OCI"),
    ("Fecha de notificación del doc con el que se envía informe a OCI", "FECHA_NOTIFICACION_OCI"),
    ("Calificación de la respuesta", "CALIFICACION_RESPUESTA"),
    ("Supuesto que concluye el seguimiento", "SUPUESTO_CIERRE"),
]

ORACLE_COLUMNS: list[str] = [name for _, name in CAMPOS] + ["ANIO"]
