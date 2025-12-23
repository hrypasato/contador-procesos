from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm

from domain.constants import filas, columnas, margen_izq_der, margen_sup_inf, espacio_entre_tablas, padding_filas

def generar_pdf(
    inicio: int,
    fin: int,
    output_path: str,
    filas: int = filas,
    columnas: int = columnas
):
    numeros_por_tabla = filas * columnas
    numeros_por_hoja = numeros_por_tabla * 2

    numeros = list(range(inicio, fin + 1))

    def construir_tabla_vertical(nums):
        tabla = [["" for _ in range(columnas)] for _ in range(filas)]
        idx = 0
        for c in range(columnas):
            for f in range(filas):
                if idx < len(nums):
                    tabla[f][c] = nums[idx]
                    idx += 1
        return tabla

    styles = getSampleStyleSheet()
    numero_style = ParagraphStyle(
        name="Numero",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=14
    )

    def convertir(tabla):
        return [
            [Paragraph(str(c), numero_style) if c != "" else "" for c in fila]
            for fila in tabla
        ]

    def crear_tabla(tabla):
        t = Table(tabla, hAlign="CENTER")
        t.setStyle(TableStyle([
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("INNERGRID", (0,0), (-1,-1), 0.5, "#BBBBBB"),
            ("BOX", (0,0), (-1,-1), 1, "#000000"),
            ("TOPPADDING", (0,0), (-1,-1), padding_filas),
            ("BOTTOMPADDING", (0,0), (-1,-1), padding_filas),
        ]))
        return t

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=margen_izq_der*cm,
        rightMargin=margen_izq_der*cm,
        topMargin=margen_sup_inf*cm,
        bottomMargin=margen_sup_inf*cm
    )

    elementos = []

    for i in range(0, len(numeros), numeros_por_hoja):
        bloque = numeros[i:i + numeros_por_hoja]

        t1 = convertir(construir_tabla_vertical(bloque[:numeros_por_tabla]))
        t2 = convertir(construir_tabla_vertical(bloque[numeros_por_tabla:]))

        elementos.append(crear_tabla(t1))
        elementos.append(Spacer(1, espacio_entre_tablas*cm))
        elementos.append(crear_tabla(t2))

        if i + numeros_por_hoja < len(numeros):
            elementos.append(PageBreak())

    doc.build(elementos)
