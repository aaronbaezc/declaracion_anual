import os
import sys
from datetime import datetime 
from decimal import Decimal
import xml.etree.ElementTree as ET

#POSICIONES XML
INDEX_COMPLEMENTO = 3
INDEX_COMPLEMENTO_NOMINA = 0
INDEX_COMPLEMENTO_NOMINA_PERCEPCIONES = 2
INDEX_COMPLEMENTO_NOMINA_DEDUCCIONES = 3

#FORMATO TEXTO
BOLD = '\033[1m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
UNDERLINE = '\033[4m'
END = '\033[0m'

#FORMATO COLUMNAS
ANCHO_COL_FECHA = 20
ANCHO_COL_PERCEPCIONES = 15
ANCHO_COL_RETENCIONES = 15
ANCHO_COL_EXENTO = 15


def encabezados():
    encabezado_fecha = 'Fecha'.ljust(ANCHO_COL_FECHA)
    encabezado_percepciones = 'Percepciones'.rjust(ANCHO_COL_PERCEPCIONES)
    encabezado_retenciones = 'Retenciones'.rjust(ANCHO_COL_RETENCIONES)
    encabezado_exento = 'Exento'.rjust(ANCHO_COL_EXENTO)

    print()
    print(BOLD + UNDERLINE + encabezado_fecha, encabezado_percepciones, encabezado_retenciones, encabezado_exento, END) 
    print()

def totales(total_percepciones, total_retenciones, total_exento):
    total_etiqueta_print = BOLD + "Totales".ljust(ANCHO_COL_FECHA)
    total_percepciones_print = GREEN + str(total_percepciones).rjust(ANCHO_COL_PERCEPCIONES)
    total_retenciones_print = RED + str(total_retenciones).rjust(ANCHO_COL_RETENCIONES)
    total_exento_print = YELLOW + str(total_exento).rjust(ANCHO_COL_EXENTO)

    print()
    print(total_etiqueta_print, total_percepciones_print, total_retenciones_print, total_exento_print, END)
    print()

def main():
    ruta_xmls = sys.argv[1] if len(sys.argv) > 1 else 0 
    anio = sys.argv[2] if len(sys.argv) > 2 else 0 

    if ruta_xmls == 0:
        print(YELLOW + 'Debe proporcionar ruta de archivos XML', END)
        return

    total_percepciones = 0
    total_retenciones = 0
    total_exento = 0

    xmlFiles = os.listdir(ruta_xmls)

    encabezados()

    for xmlFile in xmlFiles:
        if anio != 0 and not xmlFile.startswith(anio):
            continue

        tree = ET.parse('./xml/' + xmlFile)
        root = tree.getroot()

        fecha_cadena = root.attrib['Fecha']
        fecha = datetime.strptime(fecha_cadena, '%Y-%m-%dT%H:%M:%S')

        percepciones_gravadas = 0
        percepciones_exentas = 0
        impuestos_retenidos = 0

        for nodo_nomina in root[INDEX_COMPLEMENTO]:
            nodo_percepciones = nodo_nomina[INDEX_COMPLEMENTO_NOMINA_PERCEPCIONES]
            percepciones_gravadas += Decimal(nodo_percepciones.attrib['TotalGravado'])
            percepciones_exentas += Decimal(nodo_percepciones.attrib['TotalExento'])

            nodo_deducciones = nodo_nomina[INDEX_COMPLEMENTO_NOMINA_DEDUCCIONES]
            impuestos_retenidos += Decimal(nodo_deducciones.attrib['TotalImpuestosRetenidos'])


        total_percepciones += percepciones_gravadas + percepciones_exentas
        total_retenciones += impuestos_retenidos
        total_exento += percepciones_exentas

        fecha_print = fecha.strftime("%Y %B %d").ljust(ANCHO_COL_FECHA)
        percepciones_print = str(percepciones_gravadas + percepciones_exentas).rjust(ANCHO_COL_PERCEPCIONES)
        retenciones_print = str(impuestos_retenidos).rjust(ANCHO_COL_RETENCIONES)
        exento_print = str(percepciones_exentas).rjust(15)
        
        print(fecha_print, percepciones_print, retenciones_print, exento_print)
   
    totales(total_percepciones, total_retenciones, total_exento)

main()