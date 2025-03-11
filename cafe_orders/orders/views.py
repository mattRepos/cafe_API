from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError

from .models.Order import Order
from .Serializers.order_serizer import OrderSerializer
from .schemas.order import OrderCreateSchema, StatusSchema

from typing import Any
from django.shortcuts import get_object_or_404


class OrderViewSet(ViewSet):
    """
    ViewSet для управления заказами в кафе.

    Предоставляет методы для создания, чтения, обновления и удаления заказов,
    а также для расчёта выручки за смену.
    """

    def get_queryset(self) -> list[Order]:
        """
        Возвращает QuerySet всех заказов.

        Returns:
            list[Order]: Список всех заказов.
        """
        return Order.objects.all()

    def get_order_entity(self, request: Request, pk: int) -> Order:
        """
        Получает объект заказа по его ID.

        Args:
            request (Request): Запрос от клиента.
            pk (int): ID заказа.

        Returns:
            Order: Объект заказа.

        Raises:
            NotFound: Если заказ с указанным ID не найден.
        """
        try:
            return get_object_or_404(Order, pk=pk)
        except:
            raise NotFound({'detail': 'Заказ не найден'})

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Возвращает список всех заказов.

        Args:
            request (Request): Запрос от клиента.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: Ответ с данными всех заказов.
        """
        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def retrieve(self, request: Request, pk: int | None = None, *args: Any, **kwargs: Any) -> Response:
        """
        Возвращает детали конкретного заказа по его ID.

        Args:
            request (Request): Запрос от клиента.
            pk (int | None): ID заказа.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: Ответ с данными заказа.
        """
        order = self.get_order_entity(request, pk)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data, status=200)

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Создаёт новый заказ.

        Args:
            request (Request): Запрос от клиента.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: Ответ с данными созданного заказа.

        Raises:
            ValidationError: Если данные запроса не прошли валидацию.
        """
        try:
            # Валидация данных с помощью Pydantic
            data = OrderCreateSchema.model_validate(request.data)
            items = [dict(item) for item in data.items]
            total_price = sum(item['price'] for item in items)

            # Создание заказа
            order = Order.objects.create(
                table_number=data.table_number,
                items=items,
                total_price=total_price,
                status='pending'
            )
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.errors(), status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, pk: int, *args: Any, **kwargs: Any) -> Response:
        """
        Обновляет статус заказа по его ID.

        Args:
            request (Request): Запрос от клиента.
            pk (int): ID заказа.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: Ответ с данными обновлённого заказа.

        Raises:
            ValidationError: Если данные запроса не прошли валидацию.
        """
        try:
            data = StatusSchema(**request.data)
            order = self.get_order_entity(request, pk)
            order.status = data.status
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int | None = None, *args: Any, **kwargs: Any) -> Response:
        """
        Удаляет заказ по его ID.

        Args:
            request (Request): Запрос от клиента.
            pk (int | None): ID заказа.
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            Response: Пустой ответ с кодом 204 (No Content).
        """
        order = self.get_order_entity(request, pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def revenue(self, request: Request) -> Response:
        """
        Рассчитывает общую выручку за смену.

        Args:
            request (Request): Запрос от клиента.

        Returns:
            Response: Ответ с общей выручкой за смену.
        """
        from django.db.models import Sum
        total_revenue = Order.objects.filter(status='paid').aggregate(total=Sum('total_price'))['total']
        return Response({'total_revenue': total_revenue or 0}, status=200)