"""Cruza las fuentes y produce el dataset unificado del proyecto.

Dos puntos de fuentes distintas se consideran el mismo DEA cuando están a menos
de RADIO_METROS y sus nombres se parecen. El umbral es deliberadamente
conservador: ante la duda se dejan separados y quedan para verificación en
terreno, porque un duplicado se detecta después pero un DEA borrado se pierde.

Uso:
    python scripts/03_cruzar_fuentes.py
"""

import json
import math
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

RADIO_METROS = 120
SIMILITUD_MINIMA = 0.60

FUENTES = [
    ("datos/fuentes/oficial-seremi.geojson", "oficial:seremi-minsal"),
    ("datos/fuentes/comunidad-instagram.geojson", "comunidad:instagram"),
    ("datos/fuentes/osm.geojson", "osm"),
]

# Palabras que aparecen en casi todos los nombres y no distinguen un lugar de otro.
RUIDO = {
    "SUPERMERCADO", "MALL", "CENTRO", "COMERCIAL", "LIDER", "EXPRESS", "COLEGIO",
    "LICEO", "ESCUELA", "HOSPITAL", "CLINICA", "HOTEL", "ESTACION", "METRO",
    "DE", "DEL", "LA", "EL", "LOS", "LAS", "Y", "SAN", "SANTA",
}


def limpiar(nombre):
    texto = "".join(
        c for c in unicodedata.normalize("NFKD", (nombre or "").upper()) if not unicodedata.combining(c)
    )
    texto = re.sub(r"[^A-Z0-9 ]", " ", texto)
    palabras = [p for p in texto.split() if p not in RUIDO and len(p) > 2]
    return " ".join(palabras)


def metros_entre(a, b):
    """Distancia haversine en metros entre dos [lon, lat]."""
    lon1, lat1 = math.radians(a[0]), math.radians(a[1])
    lon2, lat2 = math.radians(b[0]), math.radians(b[1])
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))


def se_parecen(nombre_a, nombre_b):
    a, b = limpiar(nombre_a), limpiar(nombre_b)
    if not a or not b:
        # Sin nombre útil, la sola cercanía decide.
        return True
    if a in b or b in a:
        return True
    return SequenceMatcher(None, a, b).ratio() >= SIMILITUD_MINIMA


def celda(coord, grados=0.002):
    """Índice espacial simple: ~200 m. Evita comparar todos contra todos."""
    return (round(coord[0] / grados), round(coord[1] / grados))


def vecinas(clave):
    x, y = clave
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            yield (x + dx, y + dy)


def cargar(ruta):
    archivo = Path(ruta)
    if not archivo.exists():
        print(f"  (omitida: no existe {ruta})")
        return []
    return json.loads(archivo.read_text(encoding="utf-8"))["features"]


def fusionar(base, nuevo):
    """Agrega el nuevo rasgo al existente sin perder información."""
    propiedades = base["properties"]
    entrantes = nuevo["properties"]

    for fuente in entrantes.get("fuentes", []):
        if fuente not in propiedades["fuentes"]:
            propiedades["fuentes"].append(fuente)

    # Rellena solo los campos vacíos: la primera fuente en aportarlos manda.
    for campo in ("nombre", "direccion", "comuna", "region", "referencia", "cantidad_equipos", "osm_id"):
        if not propiedades.get(campo) and entrantes.get(campo):
            propiedades[campo] = entrantes[campo]

    if propiedades.get("tipo_recinto") in (None, "", "sin_clasificar"):
        propiedades["tipo_recinto"] = entrantes.get("tipo_recinto", "sin_clasificar")

    propiedades.setdefault("ids_origen", [propiedades["id"]])
    propiedades["ids_origen"].append(entrantes["id"])


def main():
    unificados = []
    indice = {}
    resumen = {}

    for ruta, etiqueta in FUENTES:
        print(f"Cargando {ruta}")
        rasgos = cargar(ruta)
        nuevos = fusionados = duplicados = 0

        for rasgo in rasgos:
            coord = rasgo["geometry"]["coordinates"]
            candidato = None

            for clave in vecinas(celda(coord)):
                for existente in indice.get(clave, []):
                    if metros_entre(coord, existente["geometry"]["coordinates"]) > RADIO_METROS:
                        continue
                    if se_parecen(rasgo["properties"].get("nombre"), existente["properties"].get("nombre")):
                        candidato = existente
                        break
                if candidato:
                    break

            if candidato:
                # Si la fuente ya figuraba en el punto encontrado, es un duplicado
                # dentro del mismo registro, no una confirmación independiente.
                if etiqueta in candidato["properties"]["fuentes"]:
                    duplicados += 1
                else:
                    fusionados += 1
                fusionar(candidato, rasgo)
            else:
                unificados.append(rasgo)
                indice.setdefault(celda(coord), []).append(rasgo)
                nuevos += 1

        resumen[etiqueta] = {
            "total": len(rasgos),
            "nuevos": nuevos,
            "confirman_otra_fuente": fusionados,
            "duplicados_internos": duplicados,
        }
        print(
            f"  {len(rasgos)} puntos -> {nuevos} nuevos, "
            f"{fusionados} confirman un punto de otra fuente, "
            f"{duplicados} duplicados dentro de la misma fuente"
        )

    for posicion, rasgo in enumerate(unificados, start=1):
        rasgo["properties"]["id"] = f"dea-cl-{posicion:05d}"

    salida = Path("datos/dea-chile.geojson")
    salida.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "name": "Desfibriladores en Chile - Corazón a Salvo",
                "licencia": "ODbL 1.0",
                "features": unificados,
            },
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )

    multi = sum(1 for r in unificados if len(r["properties"]["fuentes"]) > 1)
    print(f"\nTotal unificado: {len(unificados)} DEA")
    print(f"Confirmados por más de una fuente: {multi}")
    print(f"Escrito en {salida}")

    Path("datos/resumen-cruce.json").write_text(
        json.dumps({"fuentes": resumen, "total": len(unificados), "multifuente": multi}, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
