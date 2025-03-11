# Развертывание Django-приложения с PostgreSQL

## Предварительные требования
- Docker (https://docs.docker.com/get-docker/)
- Docker Compose (https://docs.docker.com/compose/install/)

## Установка и запуск
1. **Клонируй репозиторий**
   ```bash
   git clone https://github.com/ваш-репозиторий.git
   cd ваш-репозиторий
2. **Создай файл .env**
Создай файл .env в корне проекта и добавь туда:

env
DB_NAME=cafe_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

3. **Запусти контейнеры**

bash
docker-compose up --build

4. **Примени миграции**

bash
docker-compose exec web python manage.py migrate

5. **Создай суперпользователя**

bash
docker-compose exec web python manage.py createsuperuser

6. **Проверь приложение**

Django-приложение: http://localhost:8000

Админка Django: http://localhost:8000/admin

7. **Остановка и удаление контейнеров**

Остановить контейнеры:

bash
docker-compose down
Остановить и удалить данные:

bash
docker-compose down
