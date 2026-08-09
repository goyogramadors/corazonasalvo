# Cómo contribuir a Corazón a Salvo

Gracias por llegar hasta acá. Este proyecto existe porque personas comunes
fotografían desfibriladores y los comparten. **La contribución más valiosa no
es técnica**: es haber ido, mirado y anotado dónde está el equipo.

Hay tres formas de ayudar, ordenadas de la más simple a la más técnica.

## 1. Reportar o confirmar un DEA (sin cuenta, sin código)

Desde el **[mapa](https://goyogramadors.github.io/corazonasalvo/)** puedes:

- **Agregar un desfibrilador** que no esté registrado
- **Confirmar** que uno del mapa sigue en su lugar
- **Avisar que ya no está** o que la ubicación es incorrecta

También puedes mandarlo por [Instagram](https://instagram.com/cora_zona_salvo).

### Qué hace útil a un reporte

| | |
|---|---|
| 📸 **Foto del equipo** | Es la prueba. Sin foto el punto entra como "sin verificar" |
| 📍 **Ubicación exacta** | Marca el pin en el mapa o comparte tu ubicación estando ahí |
| 🚪 **Cómo llegar a él** | *"Primer piso, pasillo de cajas, entre el baño y la salida de emergencia"*. Esto es lo que hace la diferencia en una emergencia real |
| 🕐 **Cuándo se puede acceder** | ¿Está disponible 24/7 o solo en horario de atención? ¿Hay que pedirlo en recepción? |

**Nunca entres a un lugar restringido ni discutas con personal de seguridad
para conseguir una foto.** Si no puedes fotografiarlo, repórtalo igual
indicando lo que sabes.

### Sobre las fotos que envías

Al enviar una foto autorizas su publicación bajo licencia
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.es), es
decir, que cualquiera pueda reutilizarla citando la fuente. Envía fotos
**tuyas**, no de internet. Evita que aparezcan personas identificables; si
aparecen, las difuminamos antes de publicar.

## 2. Mapear en OpenStreetMap

Los datos de este proyecto se sincronizan con
[OpenStreetMap](https://www.openstreetmap.org), lo que hace que cada
desfibrilador aparezca en decenas de aplicaciones de mapas en todo el mundo.

Si quieres mapear directamente allá, la forma más simple es caminar con una de
estas apps en el teléfono:

- **[Every Door](https://every-door.app/)** — la más cómoda para agregar puntos
- **[StreetComplete](https://streetcomplete.app/)** — te propone misiones, incluye revisar si un DEA sigue existiendo

La etiqueta correcta es `emergency=defibrillator`, y conviene acompañarla de
`defibrillator:location` (la referencia dentro del edificio), `access`,
`opening_hours` e `indoor`. La
[documentación completa está acá](https://wiki.openstreetmap.org/wiki/Tag:emergency=defibrillator).

## 3. Aportar código o datos por GitHub

### Reportes puntuales

Usa las [plantillas de issue](https://github.com/goyogramadors/corazonasalvo/issues/new/choose).
Están pensadas como formularios: solo rellenas los campos.

### Cambios en los datos

Los datos se generan con los scripts de `scripts/`, **no se editan a mano**.
Si detectas un error:

1. Corrige la fuente correspondiente en `datos/fuentes/`
2. Regenera el dataset: `python scripts/03_cruzar_fuentes.py`
3. Abre un pull request explicando **de dónde sacaste la corrección**

Toda corrección necesita una fuente verificable: una foto, un oficio, una
visita en terreno. "Yo sé que está ahí" no basta, aunque probablemente sea
cierto: el valor de esta base es que cada punto se puede rastrear.

### Cambios en el código

```bash
git clone https://github.com/goyogramadors/corazonasalvo.git
cd corazonasalvo
python scripts/03_cruzar_fuentes.py   # debe correr sin errores
```

Los scripts usan solo la librería estándar de Python 3.9+ a propósito: quien
quiera reproducir la base no debería tener que instalar nada.

Antes de un cambio grande, abre un issue para conversarlo. Es más rápido
alinearse antes que rehacer trabajo después.

## Cosas que estamos necesitando

- **Verificación en terreno por comuna** — hay 3.451 puntos oficiales que nadie
  ha confirmado nunca
- **Ubicación dentro del recinto** — muchos registros oficiales dicen solo
  "Hospital X", que puede ser un edificio de varias hectáreas
- **Regiones fuera de la Metropolitana** — la cobertura comunitaria está muy
  concentrada en Santiago
- **Solicitudes por Ley de Transparencia** a servicios de salud y municipios
- **Diseño y accesibilidad del mapa** — tiene que funcionar en un teléfono, con
  mala señal y con alguien nervioso mirándolo

## Código de conducta

Trata a los demás con respeto. Este es un proyecto de salud pública hecho por
voluntarios; nadie está obligado a responder rápido ni a aceptar tu propuesta.
Se rechazan aportes con datos falsos o inventados: acá un error puede costar
una vida.
