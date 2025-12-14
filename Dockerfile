FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Comando para rodar em produção usando Gunicorn na porta 10000 (padrão do Render)
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
