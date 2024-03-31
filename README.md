# longevity_intime_test

Для запуска проекта необходимо клонировать репозиторий: 

```bash
    git clone git@github.com:pandser/stripe.git
```

Перейти в каталог backend

```bash
    cd backend
```
Запустить приложение через docker compose

```bash
    docker compose up
```
Подключиться к контейнеру backend

```bash
    docker exec -it backend-backend-1 bash
```
Сделать миграции и создать пользователя с root-правами
```bash
    python manage.py migrate

    python manage.py createsuperuser
```

Приложение будет доступно по адресу http://localhost:8000/

Доступны следующие энодпоинты:
- admin/ Админка приложения
- api/v1/auth/signup/ регистрация пользователя, получение кода подтверждения
- api/v1/token/ получения токена
- api/v1/token/refresh/ обновление токена
- api/v1/user/ список всех пользователей
- api/v1/user/<username>/ профиль пользователя
