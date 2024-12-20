# TWITTER CLONE
___

## О проекте:
1. Пользователь может добавить новый твит.
2. Пользователь может удалить свой твит.
3. Пользователь может зафоловить другого пользователя.
4. Пользователь может отписаться от другого пользователя.
5. Пользователь может отмечать твит как понравившийся.
6. Пользователь может убрать отметку «Нравится».
7. Пользователь может получить ленту из твитов отсортированных в
порядке убывания по популярности от пользователей, которых он
фоловит.
8. Твит может содержать картинку.

___
## Установка и запуск


1. Перед использованием приложения убедитесь, что на Вашем устройстве (Linux-based OS) установлены:

   - Docker 27.2.0
   - docker-compose 2.29.2

2. Клонируйте gitlab репозиторий на Ваше устройство
3. Создайте .env файл с переменными. Для примера используйте env.example из репозитория. Для запуска выполните в терминале:

    - docker-compose up
4. http://0.0.0.0:8080/ чтобы открыть главную страницу.
5. http://0.0.0.0:8000/docs чтобы получить доступ к Swagger документации API проекта.

___
## Тестирование

1. docker-compose -f test-docker-compose.yml up - Запуск тестовой базы данных
2. python -m venv venv - Подготовка виртуального окружения 
3. pip install -r app/server/requirements.txt 
4. pytest tests/
___