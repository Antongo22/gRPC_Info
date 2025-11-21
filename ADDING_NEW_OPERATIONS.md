# Добавление новых операций (вычитание, умножение, деление)

Это пошаговое руководство покажет, как добавить новые математические операции в существующий gRPC проект.

**Цель:** Добавить операции вычитания (Subtract), умножения (Multiply) и деления (Divide) к существующему калькулятору.


*Пример готового задания лежит в вестке `v2`*
---

## Шаг 1: Обновление .proto файла

Откройте файл `proto/calculator.proto` и добавьте новые методы в сервис и новые сообщения.

### Было:

```protobuf
syntax = "proto3";

package calculator;

service Calculator {
  rpc Add (AddRequest) returns (AddResponse);
}

message AddRequest {
  double number1 = 1;
  double number2 = 2;
}

message AddResponse {
  double result = 1;
}
```

### Стало:

```protobuf
syntax = "proto3";

package calculator;

service Calculator {
  rpc Add (AddRequest) returns (AddResponse);
  rpc Subtract (SubtractRequest) returns (SubtractResponse);
  rpc Multiply (MultiplyRequest) returns (MultiplyResponse);
  rpc Divide (DivideRequest) returns (DivideResponse);
}

message AddRequest {
  double number1 = 1;
  double number2 = 2;
}

message AddResponse {
  double result = 1;
}

message SubtractRequest {
  double number1 = 1;
  double number2 = 2;
}

message SubtractResponse {
  double result = 1;
}

message MultiplyRequest {
  double number1 = 1;
  double number2 = 2;
}

message MultiplyResponse {
  double result = 1;
}

message DivideRequest {
  double number1 = 1;
  double number2 = 2;
}

message DivideResponse {
  double result = 1;
  string error = 2;
}
```

**Что изменилось:**
- Добавили 3 новых RPC метода в сервис: `Subtract`, `Multiply`, `Divide`
- Добавили 6 новых сообщений (по 2 на каждую операцию: Request и Response)
- В `DivideResponse` добавили поле `error` для обработки деления на ноль

---

## Шаг 2: Регенерация Python кода

После изменения .proto файла нужно перегенерировать Python код.

### Для локальной разработки:

```bash
# Из корневой директории проекта
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./generated \
  --grpc_python_out=./generated \
  ./proto/calculator.proto
```

### Скопируйте сгенерированные файлы:

```bash
# Копируем в grpc_service
cp generated/calculator_pb2.py grpc_service/
cp generated/calculator_pb2_grpc.py grpc_service/

# Копируем в api_service
cp generated/calculator_pb2.py api_service/
cp generated/calculator_pb2_grpc.py api_service/
```

**Важно:** Если используете Docker, файлы сгенерируются автоматически при сборке образа.

---

## Шаг 3: Обновление gRPC сервера

Откройте файл `grpc_service/server.py` и добавьте реализацию новых методов в класс `CalculatorServicer`.

### Найдите класс CalculatorServicer:

```python
class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    """
    Реализация сервиса Calculator
    Наследуемся от автосгенерированного базового класса
    """
    
    def Add(self, request, context):
        """
        Метод для сложения двух чисел
        request - объект AddRequest с полями number1 и number2
        context - контекст gRPC (метаданные, статус, таймауты)
        """
        result = request.number1 + request.number2

        logger.info(f"Получен запрос: {request.number1} + {request.number2} = {result}")
        
        # Возвращаем объект AddResponse с результатом
        return calculator_pb2.AddResponse(result=result)
```

### Добавьте после метода Add:

```python
    def Subtract(self, request, context):
        """Метод для вычитания двух чисел"""
        result = request.number1 - request.number2
        logger.info(f"Получен запрос: {request.number1} - {request.number2} = {result}")
        return calculator_pb2.SubtractResponse(result=result)
    
    def Multiply(self, request, context):
        """Метод для умножения двух чисел"""
        result = request.number1 * request.number2
        logger.info(f"Получен запрос: {request.number1} * {request.number2} = {result}")
        return calculator_pb2.MultiplyResponse(result=result)
    
    def Divide(self, request, context):
        """Метод для деления двух чисел"""
        if request.number2 == 0:
            logger.warning(f"Попытка деления на ноль: {request.number1} / 0")
            return calculator_pb2.DivideResponse(
                result=0,
                error="Деление на ноль невозможно"
            )
        
        result = request.number1 / request.number2
        logger.info(f"Получен запрос: {request.number1} / {request.number2} = {result}")
        return calculator_pb2.DivideResponse(result=result, error="")
```

**Полный класс CalculatorServicer теперь выглядит так:**

```python
class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    """
    Реализация сервиса Calculator
    Наследуемся от автосгенерированного базового класса
    """
    
    def Add(self, request, context):
        """Метод для сложения двух чисел"""
        result = request.number1 + request.number2
        logger.info(f"Получен запрос: {request.number1} + {request.number2} = {result}")
        return calculator_pb2.AddResponse(result=result)
    
    def Subtract(self, request, context):
        """Метод для вычитания двух чисел"""
        result = request.number1 - request.number2
        logger.info(f"Получен запрос: {request.number1} - {request.number2} = {result}")
        return calculator_pb2.SubtractResponse(result=result)
    
    def Multiply(self, request, context):
        """Метод для умножения двух чисел"""
        result = request.number1 * request.number2
        logger.info(f"Получен запрос: {request.number1} * {request.number2} = {result}")
        return calculator_pb2.MultiplyResponse(result=result)
    
    def Divide(self, request, context):
        """Метод для деления двух чисел"""
        if request.number2 == 0:
            logger.warning(f"Попытка деления на ноль: {request.number1} / 0")
            return calculator_pb2.DivideResponse(
                result=0,
                error="Деление на ноль невозможно"
            )
        
        result = request.number1 / request.number2
        logger.info(f"Получен запрос: {request.number1} / {request.number2} = {result}")
        return calculator_pb2.DivideResponse(result=result, error="")
```

---

## Шаг 4: Обновление FastAPI сервиса

Откройте файл `api_service/main.py` и добавьте новые эндпоинты.

### 4.1. Добавьте новые Pydantic модели

Найдите существующие модели `AddRequest` и `AddResponse` и добавьте после них:

```python
class SubtractRequest(BaseModel):
    """Pydantic модель для вычитания"""
    number1: float
    number2: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "number1": 10.0,
                "number2": 3.5
            }
        }


class SubtractResponse(BaseModel):
    """Модель ответа для вычитания"""
    result: float


class MultiplyRequest(BaseModel):
    """Pydantic модель для умножения"""
    number1: float
    number2: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "number1": 4.0,
                "number2": 2.5
            }
        }


class MultiplyResponse(BaseModel):
    """Модель ответа для умножения"""
    result: float


class DivideRequest(BaseModel):
    """Pydantic модель для деления"""
    number1: float
    number2: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "number1": 10.0,
                "number2": 2.0
            }
        }


class DivideResponse(BaseModel):
    """Модель ответа для деления"""
    result: float
    error: str = ""
```

### 4.2. Добавьте новые эндпоинты

Найдите функцию `add_numbers` и добавьте после неё:

```python
@app.post("/subtract", response_model=SubtractResponse)
async def subtract_numbers(request: SubtractRequest):
    """
    Вычитание двух чисел через gRPC сервис
    
    - **number1**: первое число (уменьшаемое)
    - **number2**: второе число (вычитаемое)
    """
    try:
        with grpc.insecure_channel(GRPC_ADDRESS) as channel:
            stub = calculator_pb2_grpc.CalculatorStub(channel)
            
            grpc_request = calculator_pb2.SubtractRequest(
                number1=request.number1,
                number2=request.number2
            )
            
            grpc_response = stub.Subtract(grpc_request)
            
            return SubtractResponse(result=grpc_response.result)
            
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


@app.post("/multiply", response_model=MultiplyResponse)
async def multiply_numbers(request: MultiplyRequest):
    """
    Умножение двух чисел через gRPC сервис
    
    - **number1**: первое число
    - **number2**: второе число
    """
    try:
        with grpc.insecure_channel(GRPC_ADDRESS) as channel:
            stub = calculator_pb2_grpc.CalculatorStub(channel)
            
            grpc_request = calculator_pb2.MultiplyRequest(
                number1=request.number1,
                number2=request.number2
            )
            
            grpc_response = stub.Multiply(grpc_request)
            
            return MultiplyResponse(result=grpc_response.result)
            
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


@app.post("/divide", response_model=DivideResponse)
async def divide_numbers(request: DivideRequest):
    """
    Деление двух чисел через gRPC сервис
    
    - **number1**: первое число (делимое)
    - **number2**: второе число (делитель)
    """
    try:
        with grpc.insecure_channel(GRPC_ADDRESS) as channel:
            stub = calculator_pb2_grpc.CalculatorStub(channel)
            
            grpc_request = calculator_pb2.DivideRequest(
                number1=request.number1,
                number2=request.number2
            )
            
            grpc_response = stub.Divide(grpc_request)
            
            # Проверяем, есть ли ошибка (деление на ноль)
            if grpc_response.error:
                raise HTTPException(
                    status_code=400,
                    detail=grpc_response.error
                )
            
            return DivideResponse(
                result=grpc_response.result,
                error=grpc_response.error
            )
            
    except HTTPException:
        raise
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
```
---
# Можно тестировать!