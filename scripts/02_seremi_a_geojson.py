"""Normaliza el registro oficial de la SEREMI de Salud al GeoJSON del proyecto.

El registro se obtiene del visor público de MINSAL. Ver docs/extraccion-seremi.md
para el procedimiento de descarga.

Los campos personales que el visor expone (RUT, nombre y correo del solicitante)
NO se copian: son datos de personas naturales y no aportan a la ubicación del DEA.

Uso:
    python scripts/02_seremi_a_geojson.py datos/fuentes/seremi-crudo.json
"""

import json
import sys
import unicodedata
from pathlib import Path

# Los tipos de instalación del registro son las categorías obligadas por la
# Ley 21.156. Se mapean al mismo vocabulario que usa la capa comunitaria.
TIPOS = [
    ("CENTROS DE ATENCION DE SALUD", "salud"),
    ("ESTABLECIMIENTO COMERCIAL", "comercio"),
    ("TERMINALES DE BUSES", "transporte"),
    ("ESTABLECIMIENTOS DE EDUCACION", "educacional"),
    ("RECINTOS DEPORTIVOS", "deportivo"),
    ("ESTABLECIMIENTOS DE ALOJAMIENTO", "hotel"),
    ("CINES", "cultura"),
    ("METRO", "metro"),
    ("ESTABLECIMIENTOS PUBLICOS", "institucional"),
]


def sin_tildes(texto):
    return "".join(
        c for c in unicodedata.normalize("NFKD", (texto or "").upper()) if not unicodedata.combining(c)
    )


def normalizar_tipo(bruto):
    clave = sin_tildes(bruto)
    for prefijo, destino in TIPOS:
        if prefijo in clave:
            return destino
    return "sin_clasificar"


def armar_direccion(registro):
    partes = [registro.get("via"), registro.get("calle"), registro.get("numero")]
    return " ".join(p.strip() for p in partes if p and p.strip()).title()


def convertir(ruta_json):
    registros = json.loads(Path(ruta_json).read_text(encoding="utf-8"))
    rasgos = []
    descartados = 0

    for registro in registros:
        lat, lon = registro.get("lat"), registro.get("lon")
        if not lat or not lon:
            descartados += 1
            continue
        try:
            lat, lon = float(lat), float(lon)
        except (TypeError, ValueError):
            descartados += 1
            continue
        # Chile continental e insular: descarta coordenadas evidentemente erróneas.
        if not (-56 < lat < -17 and -110 < lon < -66):
            descartados += 1
            continue

        equipos = registro.get("equipos")
        rasgos.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [round(lon, 7), round(lat, 7)]},
                "properties": {
                    "id": f"seremi-{registro['id']}",
                    "categoria": "dea",
                    "nombre": (registro.get("nombre") or "").strip(),
                    "tipo_recinto": normalizar_tipo(registro.get("tipo")),
                    "direccion": armar_direccion(registro),
                    "comuna": (registro.get("comuna") or "").title(),
                    "region": (registro.get("region") or "").title(),
                    "referencia": (registro.get("referencia") or "").strip(),
                    "cantidad_equipos": int(equipos) if str(equipos).isdigit() else None,
                    "fuentes": ["oficial:seremi-minsal"],
                    "fecha_registro": registro.get("creado"),
                    "verificacion": {
                        "estado": "sin_verificar",
                        "confirmaciones": 0,
                        "reportes_ausencia": 0,
                        "ultima_confirmacion": None,
                    },
                },
            }
        )

    print(f"{len(rasgos)} puntos válidos, {descartados} descartados por coordenada faltante o fuera de Chile")
    return {
        "type": "FeatureCollection",
        "name": "Registro oficial de DEA - SEREMI de Salud (MINSAL)",
        "features": rasgos,
    }


if __name__ == "__main__":
    salida = Path("datos/fuentes/oficial-seremi.geojson")
    salida.parent.mkdir(parents=True, exist_ok=True)

    coleccion = convertir(sys.argv[1])
    salida.write_text(json.dumps(coleccion, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Escrito en {salida}")
