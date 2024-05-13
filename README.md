# Django-mailing

Сервис управления рассылками, администрирования и получения статистики. Есть возможность почитать блоги.

## Логика работы системы:

Анонимные пользователи не могут пользоваться сайтом.
Пользователь регистрируется, создает клиентов, письма, рассылки, у каждой рассылки есть свои логи.
Планировщик каждую минуту проверяет нужно ли отправить рассылки удовлетворяющие требованиям.
По результатам отправки формируются логи, которые видны пользователю.
Отправка писем возможна раз в сутки, раз в неделю или раз в месяц.

## Технологии

- Python 3
- Django 5
- PostgreSQL
- Redis

## Развертывание проекта

- Установить зависимости из файла pyproject.toml
- Создать базу данных
- В файле .env_example написать необходимые параметры для настройки системы
- Переименовать файл .env_example в .env
- Создать и применить миграции
- Включить сервер Redis или отключить кеширование

## Использование проекта

- (Опционально) Наполнить базу данных из фикстур
- Зарегистрировать суперпользователя можно через команду python manage.py csu
- Зарегистрировать менеджера можно через команду python manage.py manager
- Зарегистрировать тестового пользователя можно через команду python manage.py test_user
- Запуск планировщика через команду python manage.py runscheduler

### Настройки прав доступа реализованы следующим образом:

- Суперюзер - все права
- Менеджер (с флагом is_staff) - CRUD блогов (создаются через админку), может просматривать и отключать рассылки, может
  просматривать пользователей и блокировать их через отдельную страницу менеджера (кнопка внизу главной страницы).
- Юзер - CRUD клиентов, писем, рассылок (только своих)
