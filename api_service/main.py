
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import grpc
import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))

import calculator_pb2  # Содержит классы сообщений (AddRequest, AddResponse)
import calculator_pb2_grpc  # Содержит классы для gRPC клиента

app = FastAPI(
    title="Calculator API",
    description="REST API для сложения чисел через gRPC",
    version="1.0.0"
)

GRPC_HOST = os.getenv('GRPC_SERVICE_HOST', 'localhost')
GRPC_PORT = os.getenv('GRPC_SERVICE_PORT', '50051')
GRPC_ADDRESS = f'{GRPC_HOST}:{GRPC_PORT}'

print(f"Настройки: gRPC сервер на {GRPC_ADDRESS}")


class AddRequest(BaseModel):
    """
    Pydantic модель для входящего HTTP запроса
    Автоматически валидирует типы и преобразует данные
    """
    number1: float
    number2: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "number1": 5.5,
                "number2": 3.2
            }
        }


class AddResponse(BaseModel):
    """
    Pydantic модель для HTTP ответа
    """
    result: float



@app.post("/add", response_model=AddResponse)
async def add_numbers(request: AddRequest):  # Асинхронная функция-обработчик
    """
    Сложение двух чисел через gRPC сервис
    FastAPI автоматически парсит JSON и валидирует через AddRequest
    
    - **number1**: первое число
    - **number2**: второе число
    """
    try:
        # insecure_channel - незащищенное соединение (без SSL/TLS)
        with grpc.insecure_channel(GRPC_ADDRESS) as channel:
            
            # stub (клиент) для вызова удаленных процедур
            # CalculatorStub - автосгенерированный класс клиента
            stub = calculator_pb2_grpc.CalculatorStub(channel)

            grpc_request = calculator_pb2.AddRequest(
                number1=request.number1,
                number2=request.number2
            )

            # Отправляет grpc_request по сети и получает grpc_response
            grpc_response = stub.Add(grpc_request)

            return AddResponse(result=grpc_response.result)
            
    except grpc.RpcError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Ошибка связи с gRPC сервисом: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    api_host = os.getenv('API_HOST', '0.0.0.0')
    api_port = int(os.getenv('API_PORT', '8000'))

    uvicorn.run(app, host=api_host, port=api_port)
