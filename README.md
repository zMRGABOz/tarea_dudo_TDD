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

### Todos los tests con cobertura:
```bash
pytest
```

### Test específico:
```bash
pytest tests/test_dado.py
```

### Test específico con más detalle:
```bash
pytest tests/test_dado.py -vv -s
```

### Solo cobertura:
```bash
pytest --cov=src --cov-report=term-missing
```