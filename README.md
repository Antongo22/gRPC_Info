# Гайд по gRPC - Пример с FastAPI и gRPC

## Protocol Buffers использует метапрограммирование - классы создаются во время выполнения программы, а не прописаны в коде явно

📖 **[Подробный гайд по синтаксису Protocol Buffers](PROTOBUF_SYNTAX.md)**

--- 

Проект состоит из двух микросервисов:



1. **API Service (FastAPI)** - REST API сервис, который принимает HTTP запросы
2. **gRPC Service** - gRPC сервер, который выполняет вычисления

### Архитектура

```
Клиент → FastAPI → gRPC Service
```

- Клиент отправляет HTTP POST запрос на `/add` с двумя числами
- FastAPI сервис получает запрос и вызывает gRPC сервис
- gRPC сервис складывает числа и возвращает результат
- FastAPI возвращает результат клиенту

---

### 1. Proto файл (calculator.proto)

Определяет контракт между клиентом и сервером:

```protobuf
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

### 2. gRPC Server (grpc_service/server.py)

- Реализует метод `Add` из proto файла
- Слушает на порту 50051
- Выполняет сложение чисел

### 3. FastAPI Service (api_service/main.py)

- Предоставляет REST API эндпоинт `/add`
- Подключается к gRPC серверу
- Преобразует HTTP запросы в gRPC вызовы

---

## Запуск проекта

### С Docker
```bash
docker compose up --force-recreate --build
```


### Без Docker

1. Зависимости
```bash
pip install -r requirements.txt
```


2. Папка для вывода готовых файлов
```bash
mkdir -p generated
```

3. Генерация Python кода из .proto файла
```bash
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./generated \
  --grpc_python_out=./generated \
  ./proto/calculator.proto
```

**Разбор команды:**
- `python -m grpc_tools.protoc` - запуск protobuf компилятора через Python модуль
- `-I./proto` - путь к директории с .proto файлами (Input directory)
- `--python_out=./generated` - куда генерировать `calculator_pb2.py` (классы сообщений)
- `--grpc_python_out=./generated` - куда генерировать `calculator_pb2_grpc.py` (классы сервера/клиента)
- `./proto/calculator.proto` - какой .proto файл компилировать

**Результат:** создаются файлы `calculator_pb2.py` и `calculator_pb2_grpc.py` в папке `./generated`

4. Скопировать файлы в корень двух проектов


5. Запуск сервера
```bash
cd grpc_service 
python server.py
```

6. В другом терминале:
```bash
cd api_service 
uvicorn main:app --reload     
```

7. По `http://localhost:8000/docs` можно потыкать Swagger

---

## Описание файлов проекта

### Основные файлы

#### `proto/calculator.proto`
**Контракт gRPC сервиса**
- Описывает структуру сообщений (AddRequest, AddResponse)
- Определяет методы сервиса (Add)
- Используется для генерации кода на Python
- Язык описания: Protocol Buffers (protobuf)

### Сгенерированные файлы (создаются автоматически)

#### `calculator_pb2.py`
**Классы сообщений**
- Автоматически генерируется из `.proto` файла
- Содержит классы `AddRequest` и `AddResponse`
- Создается динамически через метапрограммирование
- Предоставляет методы сериализации/десериализации
- **НЕ РЕДАКТИРОВАТЬ ВРУЧНУЮ!**

#### `calculator_pb2_grpc.py`
**Классы сервера и клиента**
- Автоматически генерируется из `.proto` файла
- Содержит `CalculatorServicer` (базовый класс для сервера)
- Содержит `CalculatorStub` (класс для клиента)
- Содержит функцию `add_CalculatorServicer_to_server()`
- **НЕ РЕДАКТИРОВАТЬ ВРУЧНУЮ!**


---

# Поток данных

1. **HTTP запрос** -> `api_service/main.py` (FastAPI)
2. **Pydantic валидация** -> проверка типов данных
3. **gRPC клиент** -> создание `CalculatorStub`
4. **Сериализация** -> `AddRequest` -> бинарный формат
5. **Сетевой вызов** -> отправка на `grpc_service`
6. **gRPC сервер** -> `server.py` -> метод `Add()`
7. **Вычисление** -> `number1 + number2`
8. **Ответ** -> `AddResponse` -> бинарный формат
9. **Десериализация** -> обратно в Python объект
10. **HTTP ответ** -> JSON с результатом