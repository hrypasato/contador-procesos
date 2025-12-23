from domain.constants import NUMEROS_POR_HOJA, NUMEROD_DE_SUGERENCIA

def sugerir_final(inicio: int, paginas: int) -> int:
    """
    Devuelve el valor final recomendado según páginas.
    """
    return inicio + (NUMEROS_POR_HOJA * paginas) - 1


def opciones_sugeridas(inicio: int, max_paginas: int = NUMEROD_DE_SUGERENCIA):
    """
    Devuelve un diccionario de opciones UX donde
    la clave es el texto mostrado y el valor es el número final.
    """
    opciones = {}

    for p in range(1, max_paginas + 1):
        total = NUMEROS_POR_HOJA * p
        valor_final = sugerir_final(inicio, p)

        opciones[
            f"{p} página(s) ({total} números) → hasta {valor_final}"
        ] = valor_final

    return opciones