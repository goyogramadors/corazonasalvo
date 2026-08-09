# Cómo se obtiene el registro oficial de DEA

El Ministerio de Salud publica un visor con los desfibriladores que los
recintos declararon conforme a la Ley 21.156:

<https://seremienlinea.minsal.cl/asdigital/index.php?DEA>

El visor no ofrece un botón de descarga de los puntos, pero **los entrega
completos al navegador** para poder dibujarlos en el mapa. Es información
pública: son los mismos datos que cualquier persona ve al abrir el sitio.

## Procedimiento

1. Abre el visor en un navegador de escritorio.
2. Abre las herramientas de desarrollador (`F12`) y ve a la consola.
3. Ejecuta:

```js
xajax_iniciarMapa();
xajax_buscarLocalesDEA();
```

4. La variable global `locales` queda cargada con todos los registros. Para
   exportarla **sin los datos personales** que el visor incluye:

```js
copy(JSON.stringify(Object.values(locales).map(l => ({
  id: l.id_tramite,
  nombre: l.gl_nombre_fantasia,
  tipo: l.gl_instalacion_tipo,
  equipos: l.nr_equipos_cantidad,
  region: l.gl_instalacion_region,
  comuna: l.gl_instalacion_comuna,
  via: l.gl_instalacion_via,
  calle: l.gl_instalacion_calle,
  numero: l.nr_instalacion_numero,
  referencia: l.gl_instalacion_otro,
  lat: l.gl_instalacion_latitud,
  lon: l.gl_instalacion_longitud,
  activo: l.bo_activo,
  creado: l.fc_creacion,
  actualizado: l.fc_actualiza
}))))
```

5. Pega el resultado en `datos/fuentes/seremi-crudo.json` y corre:

```bash
python scripts/02_seremi_a_geojson.py datos/fuentes/seremi-crudo.json
python scripts/03_cruzar_fuentes.py
```

## Datos personales: qué excluimos y por qué

El visor entrega al navegador de cualquier visitante el **RUT, el nombre y el
correo electrónico** de la persona que tramitó cada inscripción, además de los
del representante legal. Son datos de personas naturales que no aportan nada a
la ubicación de un desfibrilador.

**Este proyecto no los copia, no los almacena y no los publica.** El script de
extracción los omite explícitamente y `02_seremi_a_geojson.py` solo lee los
campos de ubicación. Si detectas alguno filtrado en los datos publicados,
[avísanos](https://github.com/goyogramadors/corazonasalvo/issues) y lo
corregimos de inmediato.

Que esa exposición exista es un problema del sistema de origen, no de este
proyecto. Corresponde reportarlo por los canales que correspondan.

## Otra fuente oficial: el informe de equipos activos

El mismo sitio publica un Excel descargable con los establecimientos activos:

<https://seremienlinea.minsal.cl/asdigital/v2/index.php/NotificacionDisponibilidadEquiposDEA/General/descargarInformeEquiposDEAActivos>

No trae coordenadas, solo direcciones, pero sirve para contrastar: si un
recinto aparece ahí y no en el visor georreferenciado, hay un registro que
falta ubicar. Se conserva en `datos/fuentes/transparencia/`.

## Calidad de los datos oficiales

Del cruce de agosto de 2026:

- **3.990** registros con coordenadas de **4.000** totales
- **539** parecen duplicados: dos o más inscripciones para el mismo punto
- Muchas referencias internas están vacías o son tan genéricas que no permiten
  encontrar el equipo dentro del recinto
- Varias coordenadas apuntan al centro de la comuna y no al recinto

Nada de esto invalida la fuente: es el punto de partida más completo que
existe. Pero explica por qué el proyecto necesita verificación comunitaria.
