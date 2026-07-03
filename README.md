# Agent API

Proyecto base en Python para comenzar con UV.

## Requisitos

- Python 3.12 o superior
- UV instalado

## Instalar UV

Si aún no tienes UV instalado, puedes hacerlo con:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Inicio rápido

```bash
cd /home/paulo/proyectos/agent-api
uv sync
uv run python main.py
```

## Comandos útiles

- `uv sync`: crea o actualiza el entorno virtual y instala las dependencias.
- `uv add <paquete>`: agrega una dependencia al proyecto.
- `uv run <comando>`: ejecuta un comando dentro del entorno del proyecto.

## Estructura básica

- `main.py`: punto de entrada del proyecto.
- `pyproject.toml`: configuración del proyecto y dependencias.
