#!/bin/bash
set -e 

# Executa o init-db
flask init-db

# Executa o seed-db
flask seed-db

# Inicia a aplicação
exec python run.py
