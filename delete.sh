#!/bin/bash
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -path "*/migrations/*.pyc"  -delete
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
echo "__pycache__ deleted"
