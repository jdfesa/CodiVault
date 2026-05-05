# Detalles técnicos

Este documento resume cómo está organizada la aplicación.

## Flujo general

```text
facilito download <url>
       |
       |-- AsyncFacilito abre Chromium con Playwright
       |-- carga cookies de sesión guardadas
       |-- identifica el tipo de URL
       |-- usa un collector para extraer estructura y unidades
       |-- usa downloaders para guardar videos o páginas
       |-- FFmpeg descarga los streams HLS
```

## Módulos principales

```text
src/facilito/
  cli.py
  async_api.py
  collectors/
  downloaders/
  models.py
  utils.py
  helpers.py
```

### `cli.py`

Define los comandos Typer:

- `login`
- `logout`
- `set-cookies`
- `download`
- `interactive`

### `async_api.py`

Coordina Playwright, sesión, autenticación y descarga.

### `collectors/`

Extraen datos desde Código Facilito:

- `unit.py`: videos, artículos y quizzes individuales
- `course.py`: cursos con capítulos
- `bootcamp.py`: programas/bootcamps, incluyendo cursos o bloques anidados
- `video.py`: URL final del stream HLS

### `downloaders/`

Guardan el contenido en disco:

- `video.py`: descarga `.mp4` con FFmpeg
- `unit.py`: descarga una unidad y reutiliza videos existentes cuando aplica
- `course.py`: estructura cursos en carpetas
- `bootcamp.py`: estructura bootcamps en módulos

## Sesión

La sesión se guarda como cookies en el directorio temporal del sistema:

```text
<temp>/Facilito/state.json
```

La app considera autenticada la sesión cuando encuentra una cookie válida de Código Facilito.

## Descarga de video

El flujo de video es:

1. Playwright abre la página autenticada.
2. El collector extrae IDs o metadata del video.
3. Se construye o encuentra la URL `.m3u8`.
4. FFmpeg descarga el stream con cookies HTTP.
5. El archivo final se guarda como `.mp4`.

## Reutilización de archivos

Antes de descargar un video, `downloaders/unit.py` busca si ya existe contenido equivalente en `Facilito/`.

Esto evita bajar otra vez el mismo video cuando:

- se reanuda una descarga;
- cambió el índice del archivo;
- un bloque aparece en más de un módulo;
- una ruta vieja y una nueva apuntan al mismo contenido.

Cuando puede, usa hardlinks para no duplicar espacio en disco.

## Bootcamps con contenido anidado

Algunos programas no enlazan directamente a videos. Enlazan a:

- cursos internos;
- bloques de cursos;
- replays;
- páginas con varias unidades.

`collectors/bootcamp.py` abre cada entrada del módulo y extrae todas las unidades visibles antes de descargar. Esto evita que el bootcamp quede incompleto.

## Troubleshooting

Los errores conocidos y soluciones históricas están documentados en:

```text
TROUBLESHOOTING.md
```
