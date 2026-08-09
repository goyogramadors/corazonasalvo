# Diccionario de datos

El archivo `dea-chile.geojson` es un **FeatureCollection** de GeoJSON
([RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946)). Cada punto es un
`Feature` con geometría `Point` en coordenadas `[longitud, latitud]`, datum
WGS84.

## Campos de cada punto

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `id` | texto | sí | Identificador estable del proyecto: `dea-cl-00001` |
| `categoria` | texto | sí | Tipo de recurso. Hoy solo `dea`; ver *Otras capas* |
| `nombre` | texto | sí | Nombre del recinto donde está el equipo |
| `tipo_recinto` | texto | sí | Categoría del lugar (ver tabla siguiente) |
| `direccion` | texto | no | Calle y número |
| `comuna` | texto | no | Comuna |
| `region` | texto | no | Región |
| `referencia` | texto | no | **Dónde encontrarlo dentro del recinto.** El campo más importante del registro |
| `acceso` | texto | no | `publico`, `restringido`, `solo_personal`, `desconocido` |
| `horario` | texto | no | Cuándo es accesible, en formato [`opening_hours`](https://wiki.openstreetmap.org/wiki/Key:opening_hours) de OSM |
| `cantidad_equipos` | entero | no | Número de DEA declarados en ese recinto |
| `fuentes` | lista | sí | De dónde viene el dato (ver *Fuentes*) |
| `ids_origen` | lista | no | Identificadores en las fuentes originales |
| `osm_id` | texto | no | Nodo correspondiente en OpenStreetMap, si ya fue subido |
| `foto` | texto | no | Ruta o URL de la foto que respalda el registro |
| `fecha_registro` | fecha | no | Cuándo se declaró oficialmente, si aplica |
| `verificacion` | objeto | sí | Estado de verificación comunitaria (ver abajo) |

### `tipo_recinto`

`educacional`, `comercio`, `salud`, `salud_24h`, `metro`, `transporte`,
`deportivo`, `hotel`, `cultura`, `institucional`, `sin_clasificar`.

Las categorías siguen los recintos obligados por la Ley 21.156, para poder
medir cumplimiento por tipo de lugar.

### `fuentes`

- `oficial:seremi-minsal` — registro público de la autoridad sanitaria
- `comunidad:instagram` — reportado por una persona con foto
- `osm` — proviene de OpenStreetMap
- `transparencia:<organismo>` — respuesta a solicitud por Ley de Transparencia

Un punto puede tener varias. **Más fuentes independientes = más confianza.**

### `verificacion`

```json
"verificacion": {
  "estado": "verificado",
  "confirmaciones": 3,
  "reportes_ausencia": 0,
  "ultima_confirmacion": "2026-08-08"
}
```

| `estado` | Significado |
|---|---|
| `verificado` | Alguien confirmó presencialmente en los últimos 12 meses |
| `sin_verificar` | Está en el mapa por su fuente, pero nadie lo ha ido a ver |
| `desactualizado` | La última confirmación tiene más de 12 meses |
| `reportado_inexistente` | Alguien fue y no lo encontró. Se mantiene visible y marcado, no se borra |

Un punto no se elimina por un solo reporte negativo: se marca y queda para
revisión. Borrar es la última acción, no la primera, porque un error de
observación puede sacar del mapa un equipo que sí existe.

## Otras capas

El campo `categoria` está pensado para que el proyecto crezca más allá de los
desfibriladores manteniendo un solo esquema y un solo mapa:

| Valor | Capa | Estado |
|---|---|---|
| `dea` | Desfibriladores | activa |
| `acopio_medicamentos` | Puntos de acopio de medicamentos vencidos | propuesta |
| `bano_accesible` | Baños de accesibilidad universal | propuesta |
| `farmacia_turno` | Farmacias de turno | propuesta |
| `urgencia_24h` | Urgencias de atención continua | propuesta |

Las capas con datos que caducan rápido (stock de medicamentos, turnos) usarán
además un campo `vigencia_horas`, porque un reporte de stock nocturno vale
horas, no meses.
