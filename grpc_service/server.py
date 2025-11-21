
import grpc
from concurrent import futures
import sys
import os
import logging
from dotenv import load_dotenv


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))

import calculator_pb2  # Содержит классы сообщений (AddRequest, AddResponse)
import calculator_pb2_grpc  # Содержит классы для gRPC клиента

GRPC_PORT = os.getenv('GRPC_SERVICE_PORT', '50051')


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


def serve():
    """Функция запуска gRPC сервера"""
    logger.info("Запуск gRPC сервера")

    # gRPC сервер с пулом из 10 потоков
    # может обрабатывать до 10 запросов одновременно
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Регистрация сервиса на сервере и добавление его к серверу
    calculator_pb2_grpc.add_CalculatorServicer_to_server(
        CalculatorServicer(), server
    )

    # [::] - слушать на всех сетевых интерфейсах (IPv6)
    # insecure - без шифрования (для продакшена нужен SSL/TLS)
    server.add_insecure_port(f'[::]:{GRPC_PORT}')

    server.start()
    logger.info(f"RPC сервер запущен на порту {GRPC_PORT}")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Остановка сервера")
        server.stop(0)


# Запускаем сервер, если файл запущен напрямую (не импортирован)
if __name__ == '__main__':
    serve()
