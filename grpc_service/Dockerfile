FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY grpc_service/ /app/grpc_service/

# Генерируем proto файлы прямо в папку grpc_service
COPY proto/ /app/proto/
RUN python -m grpc_tools.protoc \
    -I/app/proto \
    --python_out=/app/grpc_service \
    --pyi_out=/app/grpc_service \
    --grpc_python_out=/app/grpc_service \
    /app/proto/calculator.proto

CMD ["python", "-u", "grpc_service/server.py"]
