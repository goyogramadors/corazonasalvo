"""Genera la versión liviana del dataset que consume el mapa web.

El archivo completo pasa de los 2 MB, demasiado para un teléfono con mala
señal justo cuando más se necesita. Esta versión conserva solo lo que el mapa
muestra y recorta los decimales a ~1 metro de precisión.

Uso:
    python scripts/04_generar_web.py
"""

import json
from pathlib import Path

ENTRADA = Path("datos/dea-chile.geojson")
SALIDA = Path("web/datos/dea-chile.min.geojson")

# Orden fijo: el mapa lee los puntos como arreglos, no como objetos, para
# ahorrar el peso de repetir 3.800 veces el nombre de cada campo.
COLUMNAS = ["id", "nombre", "tipo", "referencia", "comuna", "direccion", "estado", "fuentes", "equipos"]

# Códigos de una letra para las fuentes, por el mismo motivo.
CLAVE_FUENTES = {"oficial:seremi-minsal": "o", "comunidad:instagram": "c", "osm": "m"}


def compactar():
    datos = json.loads(ENTRADA.read_text(encoding="utf-8"))
    puntos = []

    for rasgo in datos["features"]:
        p = rasgo["properties"]
        lon, lat = rasgo["geometry"]["coordinates"]

        puntos.append(
            [
                round(lat, 5),
                round(lon, 5),
                p["id"].replace("dea-cl-", ""),
                p.get("nombre") or "",
                p.get("tipo_recinto") or "sin_clasificar",
                p.get("referencia") or "",
                p.get("comuna") or "",
                p.get("direccion") or "",
                (p.get("verificacion") or {}).get("estado") or "sin_verificar",
                "".join(CLAVE_FUENTES.get(f, "?") for f in p.get("fuentes", [])),
                p.get("cantidad_equipos") or 0,
            ]
        )

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(
        json.dumps(
            {"columnas": ["lat", "lon"] + COLUMNAS, "total": len(puntos), "puntos": puntos},
            ensure_ascii=False,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )

    peso = SALIDA.stat().st_size / 1024
    print(f"{len(puntos)} puntos en {SALIDA} ({peso:.0f} KB)")


if __name__ == "__main__":
    compactar()
