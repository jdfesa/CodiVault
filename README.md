

https://github.com/user-attachments/assets/5cb9125e-2add-4a3d-aae4-b2ff9ce47b45

<!-- markdownlint-disable MD033 MD041 -->
<div align="center">
    <img width="600" src="./assets/banner.png" alt="codi-vault Banner">
</div>

# codi-vault

CLI para descargar cursos, bootcamps y videos de Código Facilito para verlos sin conexión.

El proyecto está pensado para ejecutarse dentro de su propia carpeta, sin instalar comandos globales en tu sistema.

## Demo

[Ver video de funcionamiento](./assets/funcionamiento.mp4)

GitHub no siempre reproduce videos embebidos dentro del README. El enlace abre el demo versionado en el repositorio.

## Requisitos

| Herramienta | Uso |
|---|---|
| Python 3.10+ | Ejecutar la aplicación |
| Poetry | Crear y manejar el entorno local del proyecto |
| Playwright Chromium | Abrir Código Facilito con sesión autenticada |
| FFmpeg | Descargar y guardar streams HLS como `.mp4` |

En macOS:

```console
brew install python@3.12 ffmpeg pipx
pipx install poetry
```

En Linux:

```console
sudo apt install python3 python3-venv ffmpeg
pip install poetry
```

## Instalación

```console
git clone https://github.com/jdfesa/codi-vault.git
cd codi-vault
poetry env use python3.12
poetry install
poetry run playwright install chromium
```

El entorno virtual queda dentro del proyecto como `.venv/`, por configuración de `poetry.toml`.

## Comandos

Puedes ejecutar todo con Poetry:

```console
poetry run facilito login
poetry run facilito interactive
poetry run facilito download https://codigofacilito.com/programas/java-premium
poetry run facilito logout
```

O activar el entorno local del proyecto para acortar los comandos mientras estés trabajando dentro de esta terminal:

```console
source .venv/bin/activate
facilito login
facilito interactive
```

Esto no instala `facilito` globalmente. Solo usa el entorno local de `codi-vault`.

## Login

Puedes iniciar sesión de dos formas.

Login manual:

```console
poetry run facilito login
```

Login automático con `.env`:

```env
FACILITO_EMAIL=tu_correo@ejemplo.com
FACILITO_PASSWORD=tu_contraseña
```

Luego:

```console
poetry run facilito login
```

El archivo `.env` está ignorado por git.

## Descarga interactiva

```console
poetry run facilito interactive
```

El asistente pregunta la URL, calidad, cantidad de hilos, modo visible/oculto y si debe sobrescribir archivos existentes.

Si activaste `.venv`, puedes usar:

```console
facilito interactive
```

## Descarga manual

```console
poetry run facilito download <url>
```

Ejemplos:

```console
poetry run facilito download https://codigofacilito.com/cursos/docker
poetry run facilito download https://codigofacilito.com/programas/java-premium
poetry run facilito download https://codigofacilito.com/videos/...
```

Opciones principales:

| Opción | Descripción |
|---|---|
| `--quality`, `-q` | Calidad del video: `max`, `1080p`, `720p`, `480p`, `360p`, `min` |
| `--threads`, `-t` | Hilos de descarga, de 1 a 16 |
| `--override`, `-w` | Sobrescribe archivos existentes |
| `--headless / --no-headless` | Ejecuta el navegador oculto o visible |

Por defecto, si un archivo ya existe, se omite.

## Salida

Las descargas se guardan en:

```text
Facilito/
```

Los cursos y bootcamps se organizan por carpetas. Los videos sueltos se guardan en:

```text
Facilito/Videos Sueltos/
```

## Actualización

```console
git pull
poetry install
poetry run playwright install chromium
```

## Documentación

- [Instalación detallada](./docs/INSTALLATION.md)
- [Guía de uso](./docs/USAGE.md)
- [Detalles técnicos](./docs/TECHNICAL.md)
- [Solución de problemas](./TROUBLESHOOTING.md)

## Aviso de uso

Este proyecto se realiza con fines educativos y de aprendizaje. El código se ofrece sin garantía. Es responsabilidad del usuario utilizarlo dentro de los límites legales y éticos correspondientes.
