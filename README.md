# tarea_dudo_TDD

## Integrantes
- Gabriel Sebastián Castillo Castillo
- Braian Alejandro Urra Bastias
- Santiago Alexander Días Barra

## Instalación

Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar Tests

### Solo tests (sin cobertura):
```bash
pytest
```

### Todos los tests con cobertura:
```bash
pytest --cov=src --cov-report=term-missing
```


### Test específico:
```bash
pytest tests/test_dado.py
```

### Test específico con cobertura:
```bash
pytest tests/test_dado.py --cov=src.juego.dado --cov-report=term-missing
```