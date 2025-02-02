# test_tron_service

## Тестовое задание

Написать микросервис, который будет выводить информацию
по адресу в сети трон, его bandwidth, energy, и баланс trx.

* Ендпоинт должен принимать входные данные - адрес.

* Каждый запрос писать в базу данных, с полями о том какой кошелек запрашивался.

* Написать юнит/интеграционные тесты

* У сервиса 2 ендпоинта: POST, GET для получения списка последних записей из БД, включая пагинацию,

* 2 теста: интеграционный на ендпоинт, юнит на запись в бд

#### Примечания: 
использовать FastAPI, аннотацию(typing), SQLAlchemy ORM, для удобства с взаимодействию с троном можно использовать tronpy, для тестов Pytest

! для tronpy требуется python не выше 3.9

### СТАТУС ГОТОВНОСТИ
* не реализовано получение `energy` (честно говоря пока не нашел как получить данные сведения)


### запуск приложения

из корневой директории `uvicorn src.main:app --reload`

### запуск тестов

из корневой директории `pytest tests/`

