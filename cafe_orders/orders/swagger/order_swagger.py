from ..views import OrderViewSet  # Импортируем основной ViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..Serializers.order_serizer import OrderSerializer

class OrderSwaggerView(OrderViewSet):
    """
    Класс для Swagger-документации OrderViewSet.
    Наследуется от OrderViewSet и добавляет документацию через @swagger_auto_schema.
    """

    @swagger_auto_schema(
        tags=['order - Заказы'],
        operation_summary='Получение списка заказов',
        operation_description='Возвращает список всех заказов.',
        responses={
            200: OrderSerializer(many=True),
            500: 'Ошибка сервера'
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['order - Заказы'],
        operation_summary='Получение заказа по ID',
        operation_description='Возвращает заказ по его ID.',
        responses={
            200: OrderSerializer(),
            404: 'Заказ не найден',
            500: 'Ошибка сервера'
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['order - Заказы'],
        operation_summary='Создание заказа',
        operation_description='Создаёт новый заказ.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'table_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Номер стола'),
                'items': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Название блюда'),
                            'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Цена блюда')
                        }
                    ),
                    description='Список блюд'
                )
            }
        ),
        responses={
            201: OrderSerializer(),
            400: 'Ошибка валидации',
            500: 'Ошибка сервера'
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['order - Заказы'],
        operation_summary='Обновление статуса заказа',
        operation_description='Обновляет статус заказа по его ID.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='Статус заказа', enum=['pending', 'ready', 'paid'])
            }
        ),
        responses={
            200: OrderSerializer(),
            400: 'Ошибка валидации',
            500: 'Ошибка сервера'
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['order - Заказы'],
        operation_summary='Удаление заказа',
        operation_description='Удаляет заказ по его ID.',
        responses={
            204: 'Заказ успешно удалён',
            500: 'Ошибка сервера'
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['order - Заказы'],
        operation_summary='Расчёт выручки за смену',
        operation_description='Возвращает общую выручку за смену.',
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'total_revenue': openapi.Schema(type=openapi.TYPE_NUMBER, description='Общая выручка за смену')
                }
            ),
            500: 'Ошибка сервера'
        }
    )
    def revenue(self, request, *args, **kwargs):
        return super().revenue(request, *args, **kwargs)