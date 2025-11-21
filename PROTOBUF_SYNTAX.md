# Protocol Buffers - Синтаксис и руководство
Писал ИИ, но вроде точно.

## Что такое Protocol Buffers?

**Protocol Buffers (protobuf)** - это язык описания структуры данных от Google, который используется для сериализации структурированных данных. Это как JSON или XML, но:
- **Компактнее** - бинарный формат занимает меньше места
- **Быстрее** - сериализация/десериализация происходит быстрее
- **Строго типизирован** - ошибки находятся на этапе компиляции
- **Кроссплатформенный** - один .proto файл → код для Python, C#, Java, Go, C++, и др.

---

## Базовый синтаксис

### Структура .proto файла

```protobuf
// Версия синтаксиса (обязательно в первой строке)
syntax = "proto3";

// Пакет (namespace) для избежания конфликтов имен
package calculator;

// Импорт других .proto файлов (опционально)
import "google/protobuf/timestamp.proto";

// Определение сервиса
service Calculator {
  rpc Add (AddRequest) returns (AddResponse);
}

// Определение сообщения (структуры данных)
message AddRequest {
  double number1 = 1;
  double number2 = 2;
}

message AddResponse {
  double result = 1;
}
```

---

## Базовые команды для работы с protobuf

### Установка зависимостей

```bash
# Для Python
pip install grpcio grpcio-tools protobuf
```

### Генерация кода из .proto файла

#### Базовая команда для Python

```bash
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./generated \
  --grpc_python_out=./generated \
  ./proto/calculator.proto
```

**Разбор параметров:**

| Параметр | Описание | Пример |
|----------|----------|--------|
| `python -m grpc_tools.protoc` | Запуск protobuf компилятора | - |
| `-I<path>` или `--proto_path=<path>` | Путь к директории с .proto файлами | `-I./proto` |
| `--python_out=<path>` | Куда генерировать `*_pb2.py` (классы сообщений) | `--python_out=./generated` |
| `--grpc_python_out=<path>` | Куда генерировать `*_pb2_grpc.py` (gRPC классы) | `--grpc_python_out=./generated` |
| `<proto_file>` | Путь к .proto файлу для компиляции | `./proto/calculator.proto` |

**Результат выполнения:**
- `calculator_pb2.py` - содержит классы сообщений (AddRequest, AddResponse)
- `calculator_pb2_grpc.py` - содержит классы сервера и клиента (CalculatorServicer, CalculatorStub)

#### Генерация для нескольких файлов

```bash
# Генерация всех .proto файлов в директории
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./generated \
  --grpc_python_out=./generated \
  ./proto/*.proto
```

#### Генерация с несколькими путями импорта

```bash
python -m grpc_tools.protoc \
  -I./proto \
  -I./proto/common \
  -I./proto/services \
  --python_out=./generated \
  --grpc_python_out=./generated \
  ./proto/calculator.proto
```

### Генерация для других языков

#### Go

```bash
protoc \
  -I./proto \
  --go_out=./generated \
  --go-grpc_out=./generated \
  ./proto/calculator.proto
```

#### Java

```bash
protoc \
  -I./proto \
  --java_out=./generated \
  --grpc-java_out=./generated \
  ./proto/calculator.proto
```

#### C++

```bash
protoc \
  -I./proto \
  --cpp_out=./generated \
  --grpc_out=./generated \
  --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` \
  ./proto/calculator.proto
```

#### C#

```bash
protoc \
  -I./proto \
  --csharp_out=./generated \
  --grpc_out=./generated \
  --plugin=protoc-gen-grpc=grpc_csharp_plugin \
  ./proto/calculator.proto
```

### Проверка синтаксиса .proto файла

```bash
# Проверка без генерации кода
python -m grpc_tools.protoc \
  -I./proto \
  --descriptor_set_out=/dev/null \
  ./proto/calculator.proto
```

### Генерация с дополнительными опциями

```bash
# Генерация с mypy типами (для Python)
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./generated \
  --grpc_python_out=./generated \
  --mypy_out=./generated \
  ./proto/calculator.proto
```

### Автоматизация через Makefile

```makefile
# Makefile
PROTO_DIR = proto
OUT_DIR = generated

.PHONY: proto
proto:
	python -m grpc_tools.protoc \
		-I$(PROTO_DIR) \
		--python_out=$(OUT_DIR) \
		--grpc_python_out=$(OUT_DIR) \
		$(PROTO_DIR)/*.proto

.PHONY: clean
clean:
	rm -rf $(OUT_DIR)/*_pb2.py $(OUT_DIR)/*_pb2_grpc.py
```

**Использование:**
```bash
make proto  # Генерация
make clean  # Очистка
```

### Автоматизация через скрипт

```bash
#!/bin/bash
# generate_proto.sh

PROTO_DIR="proto"
OUT_DIR="generated"

# Создаем директорию если не существует
mkdir -p $OUT_DIR

# Генерируем код
python -m grpc_tools.protoc \
  -I$PROTO_DIR \
  --python_out=$OUT_DIR \
  --grpc_python_out=$OUT_DIR \
  $PROTO_DIR/*.proto

echo "Proto files generated successfully!"
```

**Использование:**
```bash
chmod +x generate_proto.sh
./generate_proto.sh
```

### Частые ошибки и решения

#### Ошибка: `ModuleNotFoundError: No module named 'grpc_tools'`

```bash
# Решение: установить grpc-tools
pip install grpcio-tools
```

#### Ошибка: `calculator.proto: File not found`

```bash
# Решение: проверить путь к файлу
# Убедитесь что -I указывает на правильную директорию
python -m grpc_tools.protoc -I./proto --python_out=. ./proto/calculator.proto
```

#### Ошибка: `ImportError: cannot import name 'runtime_version'`

```bash
# Решение: обновить или откатить версии
pip install --upgrade protobuf grpcio grpcio-tools
# Или использовать совместимые версии:
pip install grpcio==1.56.2 grpcio-tools==1.56.2 protobuf==4.23.4
```

---

## Типы данных

### Скалярные типы

| Proto тип | Python тип | Описание | Пример |
|-----------|------------|----------|--------|
| `double` | `float` | 64-битное число с плавающей точкой | `3.14159` |
| `float` | `float` | 32-битное число с плавающей точкой | `3.14` |
| `int32` | `int` | 32-битное целое число | `42` |
| `int64` | `int` | 64-битное целое число | `9223372036854775807` |
| `uint32` | `int` | Беззнаковое 32-битное целое | `100` |
| `uint64` | `int` | Беззнаковое 64-битное целое | `18446744073709551615` |
| `sint32` | `int` | Знаковое 32-битное (эффективнее для отрицательных) | `-42` |
| `sint64` | `int` | Знаковое 64-битное (эффективнее для отрицательных) | `-9223372036854775808` |
| `fixed32` | `int` | Фиксированный размер 32 бита | `100` |
| `fixed64` | `int` | Фиксированный размер 64 бита | `1000` |
| `bool` | `bool` | Логическое значение | `true` / `false` |
| `string` | `str` | UTF-8 строка | `"Hello, World!"` |
| `bytes` | `bytes` | Произвольные байты | `b'\x00\x01\x02'` |

### Примеры использования

```protobuf
message User {
  int32 id = 1;              // Целое число
  string name = 2;           // Строка
  string email = 3;          // Email адрес
  bool is_active = 4;        // Флаг активности
  double balance = 5;        // Баланс счета
  bytes avatar = 6;          // Аватар в бинарном виде
}
```

---

## Нумерация полей

**Каждое поле должно иметь уникальный номер** - это его идентификатор в бинарном формате.

```protobuf
message Person {
  string name = 1;      // Номер 1
  int32 age = 2;        // Номер 2
  string email = 3;     // Номер 3
}
```

### Правила нумерации:

- **1-15** - занимают 1 байт (используйте для часто используемых полей)
- **16-2047** - занимают 2 байта
- **19000-19999** - зарезервированы, нельзя использовать
- **Нельзя менять номера** после релиза - это сломает обратную совместимость

```protobuf
message Example {
  // Часто используемые поля - номера 1-15
  string id = 1;
  string name = 2;
  
  // Редко используемые - номера 16+
  string description = 16;
  string metadata = 17;
}
```

---

## Опциональные и повторяющиеся поля

### Proto3 (по умолчанию все поля опциональные)

```protobuf
message User {
  string name = 1;           // Если не указано, будет пустая строка ""
  int32 age = 2;             // Если не указано, будет 0
  bool is_active = 3;        // Если не указано, будет false
}
```

### Явное указание optional (proto3)

```protobuf
message User {
  optional string name = 1;  // Может быть не установлено
  optional int32 age = 2;    // Можно проверить, было ли установлено
}
```

### Повторяющиеся поля (массивы)

```protobuf
message ShoppingCart {
  repeated string items = 1;        // Список строк
  repeated int32 quantities = 2;    // Список чисел
}
```

**В Python:**
```python
cart = ShoppingCart()
cart.items.append("Apple")
cart.items.append("Banana")
cart.quantities.extend([5, 3])

print(cart.items)       # ['Apple', 'Banana']
print(cart.quantities)  # [5, 3]
```

---

## Вложенные сообщения

### Простая вложенность

```protobuf
message Address {
  string street = 1;
  string city = 2;
  string country = 3;
  int32 postal_code = 4;
}

message Person {
  string name = 1;
  int32 age = 2;
  Address address = 3;     // Вложенное сообщение
}
```

### Вложенное определение

```protobuf
message Person {
  string name = 1;
  
  // Определяем тип внутри Person
  message PhoneNumber {
    string number = 1;
    string type = 2;  // "mobile", "home", "work"
  }
  
  repeated PhoneNumber phones = 2;
}
```

**В Python:**
```python
person = Person()
person.name = "John"

phone = person.phones.add()
phone.number = "+1234567890"
phone.type = "mobile"
```

---

## Enum (перечисления)

```protobuf
enum Status {
  UNKNOWN = 0;      // Первое значение ВСЕГДА должно быть 0
  PENDING = 1;
  APPROVED = 2;
  REJECTED = 3;
}

message Order {
  string id = 1;
  Status status = 2;
  double amount = 3;
}
```

**В Python:**
```python
order = Order()
order.id = "ORD-123"
order.status = Status.APPROVED
order.amount = 99.99

print(order.status)  # 2
print(Status.Name(order.status))  # "APPROVED"
```

### Правила для Enum:

- Первое значение **обязательно должно быть 0**
- Значения должны быть уникальными
- Можно использовать `option allow_alias = true;` для алиасов

```protobuf
enum Status {
  option allow_alias = true;
  UNKNOWN = 0;
  STARTED = 1;
  RUNNING = 1;  // Алиас для STARTED
}
```

---

## Oneof (одно из)

Позволяет указать, что только одно поле из группы может быть установлено.

```protobuf
message Payment {
  oneof payment_method {
    string credit_card = 1;
    string paypal_email = 2;
    string bank_account = 3;
  }
  double amount = 4;
}
```

**В Python:**
```python
payment = Payment()
payment.credit_card = "1234-5678-9012-3456"
payment.amount = 100.0

# Если установить другое поле, предыдущее сбросится
payment.paypal_email = "user@example.com"
print(payment.credit_card)  # "" (пустая строка)
print(payment.paypal_email)  # "user@example.com"

# Проверка, какое поле установлено
print(payment.WhichOneof("payment_method"))  # "paypal_email"
```

---

## Map (словари)

```protobuf
message Product {
  string id = 1;
  string name = 2;
  map<string, string> attributes = 3;    // Ключ: строка, Значение: строка
  map<string, double> prices = 4;        // Ключ: строка, Значение: число
}
```

**В Python:**
```python
product = Product()
product.id = "PROD-001"
product.name = "Laptop"

# Работа с map как со словарем
product.attributes["brand"] = "Apple"
product.attributes["color"] = "Silver"

product.prices["USD"] = 1299.99
product.prices["EUR"] = 1199.99

print(product.attributes["brand"])  # "Apple"
print(product.prices["USD"])        # 1299.99
```

---

## Значения по умолчанию

В **proto3** все поля имеют значения по умолчанию:

| Тип | Значение по умолчанию |
|-----|----------------------|
| `string` | `""` (пустая строка) |
| `bytes` | `b''` (пустые байты) |
| `bool` | `false` |
| `числовые типы` | `0` |
| `enum` | первое значение (0) |
| `message` | зависит от языка (в Python - `None` или объект по умолчанию) |
| `repeated` | пустой список |
| `map` | пустой словарь |

```protobuf
message Example {
  string name = 1;      // По умолчанию: ""
  int32 count = 2;      // По умолчанию: 0
  bool active = 3;      // По умолчанию: false
}
```

---

## Комментарии

```protobuf
// Однострочный комментарий

/*
 * Многострочный
 * комментарий
 */

message User {
  string name = 1;  // Имя пользователя
  int32 age = 2;    /* Возраст */
}
```

---

## Импорт других .proto файлов

```protobuf
// common.proto
syntax = "proto3";
package common;

message Address {
  string street = 1;
  string city = 2;
}
```

```protobuf
// user.proto
syntax = "proto3";
package user;

import "common.proto";  // Импортируем другой файл

message User {
  string name = 1;
  common.Address address = 2;  // Используем импортированный тип
}
```

---

## gRPC сервисы

### Типы RPC методов

#### 1. Unary RPC (простой запрос-ответ)

```protobuf
service Calculator {
  rpc Add (AddRequest) returns (AddResponse);
}

message AddRequest {
  double a = 1;
  double b = 2;
}

message AddResponse {
  double result = 1;
}
```

#### 2. Server Streaming (сервер отправляет поток данных)

```protobuf
service FileService {
  rpc DownloadFile (FileRequest) returns (stream FileChunk);
}

message FileRequest {
  string filename = 1;
}

message FileChunk {
  bytes data = 1;
  int32 chunk_number = 2;
}
```

#### 3. Client Streaming (клиент отправляет поток данных)

```protobuf
service UploadService {
  rpc UploadFile (stream FileChunk) returns (UploadResponse);
}

message UploadResponse {
  string file_id = 1;
  int64 size = 2;
}
```

#### 4. Bidirectional Streaming (двусторонний поток)

```protobuf
service ChatService {
  rpc Chat (stream ChatMessage) returns (stream ChatMessage);
}

message ChatMessage {
  string user = 1;
  string text = 2;
  int64 timestamp = 3;
}
```

---

## Опции (Options)

### Опции файла

```protobuf
syntax = "proto3";

// Опции для генерации кода
option java_package = "com.example.calculator";
option java_outer_classname = "CalculatorProto";
option go_package = "github.com/example/calculator";
option optimize_for = SPEED;  // SPEED, CODE_SIZE, LITE_RUNTIME

package calculator;
```

### Опции поля

```protobuf
message User {
  string id = 1 [deprecated = true];  // Помечаем поле как устаревшее
  string name = 2;
}
```

---

## Зарезервированные поля

Используйте `reserved` чтобы предотвратить использование старых номеров/имен полей:

```protobuf
message User {
  reserved 2, 15, 9 to 11;           // Зарезервированные номера
  reserved "old_field", "temp_data"; // Зарезервированные имена
  
  string name = 1;
  int32 age = 3;
  // Нельзя использовать номера 2, 15, 9, 10, 11
  // Нельзя использовать имена "old_field", "temp_data"
}
```

---

## Примеры реальных сценариев

### 1. API для пользователей

```protobuf
syntax = "proto3";
package user;

import "google/protobuf/timestamp.proto";

enum UserRole {
  GUEST = 0;
  USER = 1;
  ADMIN = 2;
  MODERATOR = 3;
}

message User {
  string id = 1;
  string email = 2;
  string username = 3;
  UserRole role = 4;
  google.protobuf.Timestamp created_at = 5;
  google.protobuf.Timestamp updated_at = 6;
  map<string, string> metadata = 7;
}

message CreateUserRequest {
  string email = 1;
  string username = 2;
  string password = 3;
}

message CreateUserResponse {
  User user = 1;
  string token = 2;
}

message GetUserRequest {
  string id = 1;
}

message GetUserResponse {
  User user = 1;
}

message ListUsersRequest {
  int32 page = 1;
  int32 page_size = 2;
  string filter = 3;
}

message ListUsersResponse {
  repeated User users = 1;
  int32 total = 2;
  int32 page = 3;
}

service UserService {
  rpc CreateUser (CreateUserRequest) returns (CreateUserResponse);
  rpc GetUser (GetUserRequest) returns (GetUserResponse);
  rpc ListUsers (ListUsersRequest) returns (ListUsersResponse);
}
```

### 2. API для заказов

```protobuf
syntax = "proto3";
package order;

import "google/protobuf/timestamp.proto";

enum OrderStatus {
  PENDING = 0;
  CONFIRMED = 1;
  SHIPPED = 2;
  DELIVERED = 3;
  CANCELLED = 4;
}

message Product {
  string id = 1;
  string name = 2;
  double price = 3;
  int32 quantity = 4;
}

message Address {
  string street = 1;
  string city = 2;
  string state = 3;
  string country = 4;
  string postal_code = 5;
}

message Order {
  string id = 1;
  string user_id = 2;
  repeated Product products = 3;
  Address shipping_address = 4;
  OrderStatus status = 5;
  double total_amount = 6;
  google.protobuf.Timestamp created_at = 7;
  google.protobuf.Timestamp updated_at = 8;
}

message CreateOrderRequest {
  string user_id = 1;
  repeated Product products = 2;
  Address shipping_address = 3;
}

message CreateOrderResponse {
  Order order = 1;
}

message GetOrderRequest {
  string order_id = 1;
}

message GetOrderResponse {
  Order order = 1;
}

message UpdateOrderStatusRequest {
  string order_id = 1;
  OrderStatus new_status = 2;
}

message UpdateOrderStatusResponse {
  Order order = 1;
}

service OrderService {
  rpc CreateOrder (CreateOrderRequest) returns (CreateOrderResponse);
  rpc GetOrder (GetOrderRequest) returns (GetOrderResponse);
  rpc UpdateOrderStatus (UpdateOrderStatusRequest) returns (UpdateOrderStatusResponse);
}
```

---

## Best Practices (Лучшие практики)

### ✅ DO (Делайте так)

1. **Используйте осмысленные имена**
   ```protobuf
   message User {
     string email = 1;  // ✅ Понятно
   }
   ```

2. **Номера 1-15 для частых полей**
   ```protobuf
   message User {
     string id = 1;      // ✅ Часто используется
     string name = 2;    // ✅ Часто используется
     string bio = 100;   // ✅ Редко используется
   }
   ```

3. **Используйте repeated вместо массивов**
   ```protobuf
   message Cart {
     repeated string items = 1;  // ✅ Правильно
   }
   ```

4. **Добавляйте комментарии**
   ```protobuf
   message User {
     string id = 1;  // Уникальный идентификатор пользователя
   }
   ```

5. **Группируйте связанные поля**
   ```protobuf
   message User {
     // Основная информация
     string id = 1;
     string name = 2;
     
     // Контактные данные
     string email = 3;
     string phone = 4;
   }
   ```

### ❌ DON'T (Не делайте так)

1. **Не меняйте номера полей**
   ```protobuf
   message User {
     string name = 1;  // ❌ Не меняйте на 2!
   }
   ```

2. **Не используйте зарезервированные номера**
   ```protobuf
   message User {
     string field = 19000;  // ❌ Зарезервировано!
   }
   ```

3. **Не удаляйте поля без reserved**
   ```protobuf
   message User {
     // string old_field = 2;  // ❌ Плохо! Используйте reserved
     reserved 2;               // ✅ Правильно
   }
   ```

---
