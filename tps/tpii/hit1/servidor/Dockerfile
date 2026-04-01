FROM python:3.12-slim

WORKDIR /app

COPY requisitos.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requisitos.txt

COPY . ./servidor
COPY ../common/ .

EXPOSE 8000

CMD ["cd", "servidor"]
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]
