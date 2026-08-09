"""Valida el dataset antes de aceptar un cambio.

Corre en cada pull request. Si algo falla, el aporte no se mezcla hasta
corregirlo. Termina con código 1 si hay errores.

Uso:
    python scripts/validar_datos.py
"""

import json
import sys
from pathlib import Path

ARCHIVO = Path("datos/dea-chile.geojson")

CAMPOS_OBLIGATORIOS = ("id", "categoria", "nombre", "tipo_recinto", "fuentes", "verificacion")

TIPOS_RECINTO = {
    "educacional", "comercio", "salud", "salud_24h", "metro", "transporte",
    "deportivo", "hotel", "cultura", "institucional", "sin_clasificar",
}

ESTADOS = {"verificado", "sin_verificar", "desactualizado", "reportado_inexistente"}

# Chile continental, insular y antártico.
LAT_MIN, LAT_MAX = -90.0, -17.0
LON_MIN, LON_MAX = -110.0, -66.0


def validar():
    errores = []
    avisos = []

    if not ARCHIVO.exists():
        return [f"No existe {ARCHIVO}. Corre scripts/03_cruzar_fuentes.py"], []

    try:
        datos = json.loads(ARCHIVO.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"El GeoJSON no es válido: {e}"], []

    if datos.get("type") != "FeatureCollection":
        errores.append("El archivo debe ser un FeatureCollection")

    rasgos = datos.get("features", [])
    if not rasgos:
        errores.append("El dataset está vacío")

    vistos = set()

    for i, rasgo in enumerate(rasgos):
        etiqueta = rasgo.get("properties", {}).get("id", f"posición {i}")
        propiedades = rasgo.get("properties", {})

        for campo in CAMPOS_OBLIGATORIOS:
            if campo not in propiedades:
                errores.append(f"{etiqueta}: falta el campo obligatorio '{campo}'")

        identificador = propiedades.get("id")
        if identificador in vistos:
            errores.append(f"{etiqueta}: identificador duplicado")
        vistos.add(identificador)

        geometria = rasgo.get("geometry") or {}
        if geometria.get("type") != "Point":
            errores.append(f"{etiqueta}: la geometría debe ser Point")
            continue

        coordenadas = geometria.get("coordinates") or []
        if len(coordenadas) < 2:
            errores.append(f"{etiqueta}: coordenadas incompletas")
            continue

        lon, lat = coordenadas[0], coordenadas[1]
        if not (LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX):
            errores.append(f"{etiqueta}: coordenadas fuera de Chile ({lat}, {lon})")

        tipo = propiedades.get("tipo_recinto")
        if tipo and tipo not in TIPOS_RECINTO:
            errores.append(f"{etiqueta}: tipo_recinto desconocido '{tipo}'")

        verificacion = propiedades.get("verificacion") or {}
        estado = verificacion.get("estado")
        if estado and estado not in ESTADOS:
            errores.append(f"{etiqueta}: estado de verificación desconocido '{estado}'")

        if not propiedades.get("fuentes"):
            errores.append(f"{etiqueta}: todo punto debe declarar al menos una fuente")

        if not (propiedades.get("nombre") or "").strip():
            avisos.append(f"{etiqueta}: sin nombre de recinto")

        if not (propiedades.get("referencia") or "").strip():
            avisos.append(f"{etiqueta}: sin referencia de ubicación dentro del recinto")

    return errores, avisos


if __name__ == "__main__":
    errores, avisos = validar()

    if avisos:
        print(f"{len(avisos)} avisos (no bloquean, pero conviene completarlos):")
        for aviso in avisos[:10]:
            print(f"  · {aviso}")
        if len(avisos) > 10:
            print(f"  · ... y {len(avisos) - 10} más")
        print()

    if errores:
        print(f"{len(errores)} errores:")
        for error in errores[:40]:
            print(f"  ✗ {error}")
        if len(errores) > 40:
            print(f"  ✗ ... y {len(errores) - 40} más")
        sys.exit(1)

    print("Datos válidos.")
