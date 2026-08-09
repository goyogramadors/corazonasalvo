# ❤️ Corazón a Salvo

**El mapa abierto de desfibriladores (DEA) de Chile.**

Cuando alguien sufre un paro cardíaco, cada minuto sin desfibrilar reduce la
probabilidad de sobrevivir en cerca de un 10%. En Chile hay miles de
desfibriladores instalados por ley, pero hasta ahora no existía una forma
simple de saber **dónde está el más cercano**.

Este repositorio contiene esa base de datos, abierta y descargable por
cualquiera.

🗺️ **[Ver el mapa](https://goyogramadors.github.io/corazonasalvo/)** ·
📸 **[Instagram @corazonasalvo](https://instagram.com/corazonasalvo)** ·
📥 **[Descargar los datos](datos/dea-chile.geojson)**

---

## El estado de los datos

**3.804 desfibriladores georreferenciados en todo Chile**, construidos cruzando
tres fuentes independientes:

| Fuente | Aporta | Puntos únicos | Confirma otros |
|---|---|---:|---:|
| Registro oficial SEREMI de Salud | Recintos que declararon su DEA por ley | 3.451 | — |
| Comunidad (Instagram @corazonasalvo) | Fotos y ubicaciones enviadas por personas | **313** | 572 |
| OpenStreetMap Chile | Mapeo colaborativo previo | 40 | 18 |

Tres cosas que solo se ven al cruzar las fuentes:

- **313 desfibriladores existen en este mapa y no en el registro oficial.** Son
  equipos reales, fotografiados por personas, que el Estado no tiene
  registrados.
- **572 registros oficiales fueron confirmados en terreno** por alguien que fue,
  lo vio y lo fotografió.
- **539 registros del listado oficial parecen estar duplicados** (dos o más
  inscripciones para el mismo punto). Es un problema de calidad del dato público
  que este cruce deja a la vista.

Antes de este proyecto, OpenStreetMap tenía **67** desfibriladores registrados
en todo Chile.

## Cómo ayudar

No necesitas saber programar ni tener cuenta de GitHub.

### 1. Reportar un desfibrilador que viste

La forma más simple: **[envía el reporte desde el mapa](https://goyogramadors.github.io/corazonasalvo/)**
o mándanos la foto por [Instagram](https://instagram.com/corazonasalvo).

Lo que necesitamos: una **foto del DEA**, el **lugar** donde está, y sobre todo
una **referencia precisa** de dónde encontrarlo ("en el pasillo de cajas, al
lado del baño"). Un DEA mal ubicado dentro de un edificio gigante es casi
inútil en una emergencia.

### 2. Confirmar o desmentir uno que ya está en el mapa

Un desfibrilador registrado hace tres años puede que ya no esté. Por eso cada
punto muestra cuándo fue verificado por última vez, y cualquiera puede
confirmar que sigue ahí (o avisar que ya no está). **Los reportes negativos son
tan valiosos como los positivos**: un mapa que envía a alguien a buscar un DEA
que no existe es peor que no tener mapa.

### 3. Aportar al código o los datos

Si te mueves con Git, revisa [CONTRIBUTING.md](CONTRIBUTING.md). Hay tareas
abiertas etiquetadas [`buena primera tarea`](https://github.com/goyogramadors/corazonasalvo/labels/buena%20primera%20tarea).

## Los datos

El archivo principal es [`datos/dea-chile.geojson`](datos/dea-chile.geojson),
en formato GeoJSON estándar. Se abre directamente en QGIS, Google Earth,
Leaflet, o cualquier librería de mapas. El diccionario de campos está en
[`datos/esquema.md`](datos/esquema.md).

Cada punto declara **de qué fuente viene** y **cuándo fue verificado por última
vez**. Nada en este mapa es anónimo en su origen: si un dato está, se puede
rastrear hasta el oficio, la foto o el registro que lo respalda.

Las fuentes originales, sin procesar, están en [`datos/fuentes/`](datos/fuentes/)
— incluidos los oficios de transparencia y los archivos oficiales tal como
llegaron.

### Reconstruir la base desde cero

```bash
python scripts/00_osm_a_geojson.py
python scripts/01_kml_a_geojson.py datos/fuentes/mymaps-original.kml
python scripts/02_seremi_a_geojson.py datos/fuentes/seremi-crudo.json
python scripts/03_cruzar_fuentes.py
```

## Por qué esto es necesario

La [Ley 21.156](https://www.bcn.cl/leychile/navegar?idNorma=1131706) (2019) y su
[reglamento](https://dipol.minsal.cl/reglamento-sobre-la-obligacion-de-disponer-de-desfibriladores/)
obligan a tener desfibriladores en colegios, metros, terminales, malls,
gimnasios, cines y otros recintos de alta afluencia. Los recintos deben
declararlos a la autoridad sanitaria.

Ese registro existe, pero tiene límites: no cubre los DEA instalados
voluntariamente, la ubicación dentro del recinto suele ser imprecisa o estar
equivocada, y nadie verifica si el equipo sigue instalado y operativo. Este
proyecto no reemplaza al registro oficial: **lo complementa, lo corrige y lo
pone en un formato que cualquiera puede usar**.

## Licencias

Dos licencias, porque son dos cosas distintas:

- **Datos** ([`datos/LICENSE`](datos/LICENSE)): Open Database License (ODbL)
  v1.0 — la misma de OpenStreetMap. Úsalos libremente, incluso comercialmente;
  solo atribuye y mantén abiertas las bases derivadas.
- **Código** ([`LICENSE`](LICENSE)): MIT.
- **Fotos enviadas por la comunidad**: quien las envía autoriza su publicación
  bajo CC BY-SA 4.0. Ver [CONTRIBUTING.md](CONTRIBUTING.md).

## Aviso

Esta es información de referencia construida colaborativamente, **no un
servicio de emergencia**. Ante un paro cardíaco llama al **131 (SAMU)** de
inmediato y sigue sus instrucciones. No podemos garantizar que un DEA del mapa
esté presente, operativo o accesible en un momento dado.

## Créditos

Proyecto iniciado y mantenido por [@goyogramadors](https://github.com/goyogramadors),
con los aportes de la comunidad de [@corazonasalvo](https://instagram.com/corazonasalvo).

Fuentes de datos: SEREMI de Salud / MINSAL (registro público de DEA),
colaboradores de OpenStreetMap, y las personas que fotografiaron cada uno de
estos desfibriladores.
