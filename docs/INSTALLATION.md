# Instalación detallada

Esta guía explica formas de instalar `codi-vault` sin ensuciar tu máquina con comandos globales del proyecto.

## Opción recomendada: Poetry

`poetry.toml` configura el entorno virtual dentro del repositorio:

```toml
[virtualenvs]
in-project = true
```

Eso significa que Poetry creará `.venv/` dentro de `codi-vault`.

```console
git clone https://github.com/jdfesa/codi-vault.git
cd codi-vault
poetry env use python3.12
poetry install
poetry run playwright install chromium
```

Uso sin activar el entorno:

```console
poetry run facilito interactive
```

Uso activando el entorno local:

```console
source .venv/bin/activate
facilito interactive
```

La activación solo afecta la terminal actual.

## Alternativa: venv + pip

```console
git clone https://github.com/jdfesa/codi-vault.git
cd codi-vault

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
playwright install chromium
```

Con `.venv` activo:

```console
facilito --help
```

## Dependencias del sistema

### macOS

```console
brew install python@3.12 ffmpeg pipx
pipx install poetry
```

### Ubuntu/Debian

```console
sudo apt update
sudo apt install python3 python3-venv ffmpeg
pip install poetry
```

### Arch Linux

```console
sudo pacman -S python ffmpeg
pip install poetry
```

## Notas sobre FFmpeg

FFmpeg es obligatorio. La app usa Playwright para obtener la URL del stream, pero FFmpeg descarga el video final.

Comprueba que esté instalado:

```console
ffmpeg -version
```

## Notas sobre Playwright

Después de instalar dependencias Python, instala Chromium:

```console
poetry run playwright install chromium
```

Si usas `.venv` activado:

```console
playwright install chromium
```

## Actualizar una instalación existente

```console
cd codi-vault
git pull
poetry install
poetry run playwright install chromium
```
