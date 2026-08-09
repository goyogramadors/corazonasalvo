"""Convierte el KML exportado de Google My Maps al GeoJSON del proyecto.

Uso:
    python scripts/01_kml_a_geojson.py fuentes/instagram/mymaps.kml
"""

import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {"kml": "http://www.opengis.net/kml/2.2"}

# El campo "Tipo" de My Maps se normaliza al vocabulario del proyecto.
# Ver datos/esquema.md para la lista completa de tipos de recinto.
TIPOS = {
    "EDUCACIONAL": "educacional",
    "COMERCIO": "comercio",
    "SALUD": "salud",
    "SALUD - FUNCIONAMIENTO 24H": "salud_24h",
    "METRO": "metro",
    "HOTEL": "hotel",
    "RECINTO DEPORTIVO": "deportivo",
    "CINES, TEATROS, ETC.": "cultura",
    "INSTITUCIONES": "institucional",
    "TERMINALES DE TRANSPORTE": "transporte",
}


def texto(elemento, ruta):
    hijo = elemento.find(ruta, NS)
    return hijo.text.strip() if hijo is not None and hijo.text else ""


def dato_extendido(placemark, nombre):
    for data in placemark.findall(".//kml:Data", NS):
        if data.get("name") == nombre:
            return texto(data, "kml:value")
    return ""


def normalizar_tipo(bruto):
    if not bruto:
        return "sin_clasificar"
    clave = unicodedata.normalize("NFKD", bruto.upper().strip())
    clave = "".join(c for c in clave if not unicodedata.combining(c))
    for original, destino in TIPOS.items():
        original_sin_tilde = "".join(
            c for c in unicodedata.normalize("NFKD", original) if not unicodedata.combining(c)
        )
        if clave == original_sin_tilde:
            return destino
    return "sin_clasificar"


def convertir(ruta_kml):
    raiz = ET.parse(ruta_kml).getroot()
    rasgos = []

    for i, placemark in enumerate(raiz.findall(".//kml:Placemark", NS), start=1):
        coordenadas = texto(placemark, ".//kml:Point/kml:coordinates")
        if not coordenadas:
            continue
        partes = coordenadas.split(",")
        lon, lat = float(partes[0]), float(partes[1])

        nombre = texto(placemark, "kml:name")
        descripcion = dato_extendido(placemark, "descripción")
        # My Maps deja restos de HTML en la descripción.
        descripcion = re.sub(r"<[^>]+>", " ", descripcion).strip()

        rasgos.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [round(lon, 7), round(lat, 7)]},
                "properties": {
                    "id": f"ig-{i:04d}",
                    "categoria": "dea",
                    "nombre": nombre,
                    "tipo_recinto": normalizar_tipo(dato_extendido(placemark, "Tipo")),
                    "referencia": descripcion,
                    "fuentes": ["comunidad:instagram"],
                    "verificacion": {
                        "estado": "sin_verificar",
                        "confirmaciones": 0,
                        "reportes_ausencia": 0,
                        "ultima_confirmacion": None,
                    },
                },
            }
        )

    return {
        "type": "FeatureCollection",
        "name": "DEA reportados por la comunidad (Instagram @cora_zona_salvo)",
        "features": rasgos,
    }


if __name__ == "__main__":
    entrada = Path(sys.argv[1])
    salida = Path("datos/fuentes/comunidad-instagram.geojson")
    salida.parent.mkdir(parents=True, exist_ok=True)

    coleccion = convertir(entrada)
    salida.write_text(json.dumps(coleccion, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(coleccion['features'])} puntos escritos en {salida}")
