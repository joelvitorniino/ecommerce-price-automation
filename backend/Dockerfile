# Usa imagem base com Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia requirements e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código do app
COPY . .

# Expõe a porta usada pelo Flask
EXPOSE 8000

# Comando padrão para rodar a aplicação
CMD ["python", "run.py"]
