# **API YAMDB**
___
Проект YaMDb собирает отзывы пользователей на произведения. 
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть 
фильм или послушать музыку.
___
### Быстрый старт:
Для создания локальной копии репозитория, выполните команду:

```
git clone https://github.com/AndreyDogadkin/api_yamdb.git
```
___
Разверните и активируйте виртуальное окружение:

``python -m venv venv``

Linux, macOS: ``source venv/bin/activate``

Windows: ``venv\Scripts\activate.bat``
___

Установите зависимости проекта:
```
pip install -r requirements.txt
```
___
Выполните миграции:
```
python manage.py migrate
```
Если вам необходимы тестовые данные в базе данных, выполните команду:
```
python manage.py load_csv
```
___
Запустите сервер:

```
python manage.py runserver
```
___
Документация API расположена по адресу:

`http:<ваш адрес сервера>:<порт>/redoc/`

по умолчанию:

`http://127.0.0.1:8000/redoc/`
___