# Bot для Сервиса PythonMeetup

Бот позволяет задавать вопросы спикеру, посмотреть мероприятия, 
прочитать о Сервисе PythonMeetup, сделать рассылку пользователям бота и докладчикам, создавать новые мероприятия


### Как установить

* Скачать [этот script]([https://github.com/miazigoo/](https://github.com/miazigoo/PythonMeetup))

**Python3 уже должен быть установлен**. 
Используйте `pip` (или `pip3`, если возникает конфликт с Python2) для установки зависимостей:
```sh
pip install -r requirements.txt
```
Создайте базу данных SQLite:

```sh
python manage.py makemigrations
python manage.py migrate
```

###Если хотите работать с админ панелью:

Создайте супер пользователя (администратора) командой:
```sh
python manage.py createcuperuser
```

Запустить сервер:
```sh
python manage.py runserver
```
1. Перейти по ссылке [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)


### Как запустить:

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.
Доступны 2 переменные:
- `TELEGRAM_BOT_API_KEY` — Получите токен у [@BotFather](https://t.me/BotFather), вставте в `.env` например: `TELEGRAM_BOT_API_KEY=588535421721:AAFYtrO5YJhpUEXgyw6r1tr5fqZYY8ogS45I2E`.
- `TELEGRAM_ADMIN_ID` - Получите свой ID у [@userinfobot](https://t.me/userinfobot)

Запуск производится командой: 
```sh
python manage.py bot
```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
