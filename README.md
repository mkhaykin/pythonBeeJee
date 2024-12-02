# pythonBeeJee

Данный репозиторий - часть тестового задания (backend).
[Репозиторий frontend](https://github.com/mkhaikin/reactBeeJee)

Стек: python 3.12, flask, flask-api, jwt, postgres.

## Тестовое задание.
Необходимо создать приложение-задачник (ToDo list).
Backend на Python (Flask), frontend на React c использованием центрального хранилища (redux, mobx или context provider). К дизайну особых требований нет, должно быть аккуратно.

Задачи состоят из:
- имени пользователя;
- е-mail;
- текста задачи. 

[Полное описание](docs/taskBeeJee.md).


## Тестирование решения.
На момент сдачи проекта проект развернут [self-hosted](https://beejee.khaykin.app).
Работу API можно проверить по https://beejee.khaykin.app/api/docs


### Переменные среды:
Для запуска и тестирования проекта, требуется создать файл `.env` с переменными окружения.\
Пример файла: [`.env.example`](.env.example)

- `POSTGRES_HOST` - имя хоста
- `POSTGRES_PORT` - порт
- `POSTGRES_DB` - имя базы данных
- `POSTGRES_USER` - пользователь
- `POSTGRES_PASSWORD` - пароль   
 
- `SECRET_KEY`- ключ
- `JWT_SECRET_KEY` - ключ
- `JWT_TOKEN_LOCATION`

### Запуск через docker:
```sh
docker-compose up -d
```
Перед выполнением создайте файл переменных окружения (`.env`).\
Пример файла см. [Переменные среды](#Переменные-среды).
