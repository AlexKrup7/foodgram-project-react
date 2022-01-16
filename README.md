![foodgram_workflow](https://github.com/AlexKrup7/foodgram-project-react/workflows/foodgram_workflow/badge.svg)
*** 

## Дипломный проект курса Python-разработчик Яндекс-Практикум

***
***

### Foodgram - сервис, с помощью которого, пользователи могут делиться своими рецептами, добавлять понравившиеся рецепты в избранное, подписываться на авторов интересных рецептов, а так же скачивать список продуктов, необходимых для приготовления выбранного блюда.

***
### Проект доступен по ссылке:

www.axelsocial.ru

### Технологии
```
Python 3
Django
Django REST Framework
Djoser
Docker
```

## Запуск проекта:
1. Скачать проект по адресу:
https://github.com/AlexKrup7/foodgram-project-react.git

2. Установка docker и docker-compose
Инструкция по установке доступна в официальной инструкции

3. Создать файл .env с переменными окружения
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres # Имя базы данных
POSTGRES_USER=postgres # Администратор базы данных
POSTGRES_PASSWORD=postgres # Пароль администратора
DB_HOST=db
DB_PORT=5432
SECRET_KEY=SECRET_KEY - секретный ключ шифрования Django
```
3. Сборка и запуск контейнера
docker-compose up -d --build
4. Миграции
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
5. Сбор статики
docker-compose exec web python manage.py collectstatic --noinput
6. Создание суперпользователя Django
docker-compose exec web python manage.py createsuperuser


#### Разработчик: Алексей Крупин
https://t.me/AlohaNipurk