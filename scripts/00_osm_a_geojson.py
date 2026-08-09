"""Descarga los DEA que ya existen en OpenStreetMap para Chile y los normaliza.

Sirve para dos cosas: no duplicar lo que la comunidad OSM ya mapeó, y saber qué
puntos nuestros faltan por subir allá.

Uso:
    python scripts/00_osm_a_geojson.py            # descarga en vivo
    python scripts/00_osm_a_geojson.py --local    # usa datos/fuentes/osm-crudo.json
"""

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

OVERPASS = "https://overpass-api.de/api/interpreter"
CONSULTA = """
[out:json][timeout:90];
area["ISO3166-1"="CL"][admin_level=2]->.cl;
node["emergency"="defibrillator"](area.cl);
out body;
"""

CRUDO = Path("datos/fuentes/osm-crudo.json")


def descargar():
    datos = urllib.parse.urlencode({"data": CONSULTA}).encode()
    with urllib.request.urlopen(urllib.request.Request(OVERPASS, data=datos), timeout=120) as respuesta:
        return json.loads(respuesta.read().decode("utf-8"))


def convertir(crudo):
    rasgos = []
    for nodo in crudo["elements"]:
        etiquetas = nodo.get("tags", {})
        rasgos.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [round(nodo["lon"], 7), round(nodo["lat"], 7)]},
                "properties": {
                    "id": f"osm-{nodo['id']}",
                    "categoria": "dea",
                    "nombre": etiquetas.get("name", ""),
                    "tipo_recinto": "sin_clasificar",
                    "referencia": etiquetas.get("defibrillator:location", ""),
                    "acceso": etiquetas.get("access", ""),
                    "horario": etiquetas.get("opening_hours", ""),
                    "osm_id": f"node/{nodo['id']}",
                    "fuentes": ["osm"],
                    "verificacion": {
                        "estado": "sin_verificar",
                        "confirmaciones": 0,
                        "reportes_ausencia": 0,
                        "ultima_confirmacion": etiquetas.get("check_date"),
                    },
                },
            }
        )
    return {"type": "FeatureCollection", "name": "DEA en OpenStreetMap - Chile", "features": rasgos}


if __name__ == "__main__":
    if "--local" in sys.argv and CRUDO.exists():
        crudo = json.loads(CRUDO.read_text(encoding="utf-8"))
    else:
        crudo = descargar()
        CRUDO.parent.mkdir(parents=True, exist_ok=True)
        CRUDO.write_text(json.dumps(crudo, ensure_ascii=False), encoding="utf-8")

    coleccion = convertir(crudo)
    salida = Path("datos/fuentes/osm.geojson")
    salida.write_text(json.dumps(coleccion, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(coleccion['features'])} puntos de OSM escritos en {salida}")
