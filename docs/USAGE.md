# Guía de uso

## Ver ayuda

```console
poetry run facilito --help
```

Con `.venv` activo:

```console
facilito --help
```

## Login

Login manual:

```console
poetry run facilito login
```

Login automático con `.env`:

```env
FACILITO_EMAIL=tu_correo@ejemplo.com
FACILITO_PASSWORD=tu_contraseña
```

Después:

```console
poetry run facilito login
```

## Login con cookies

Si el login normal falla por captcha o bloqueo persistente, puedes importar cookies:

```console
poetry run facilito set-cookies path/to/cookies.json
```

El archivo debe estar en formato JSON compatible con Playwright.

## Logout

```console
poetry run facilito logout
```

## Modo interactivo

```console
poetry run facilito interactive
```

El asistente solicita:

1. URL del recurso
2. Calidad
3. Hilos de descarga
4. Modo oculto o visible
5. Sobrescritura de archivos existentes

Si Código Facilito muestra Cloudflare o errores intermitentes en modo oculto, usa modo visible.

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

## Opciones

```console
poetry run facilito download <url> --quality 720p --threads 5
```

| Opción | Alias | Descripción |
|---|---|---|
| `--quality` | `-q` | Calidad del video |
| `--threads` | `-t` | Cantidad de hilos de descarga |
| `--override` | `-w` | Sobrescribe archivos existentes |
| `--headless / --no-headless` | | Navegador oculto o visible |

## Reanudar descargas

Si una descarga se interrumpe, ejecuta el mismo comando otra vez.

Mientras no uses `--override`, los archivos existentes se omiten. En bootcamps, la app también intenta reutilizar videos ya descargados cuando el mismo contenido aparece con otra ruta o nombre.

## Carpeta de salida

```text
Facilito/
```

Ejemplo:

```text
Facilito/
  curso-profesional-de-docker/
  bootcamp-premium-de-java-profesional/
  Videos Sueltos/
```
