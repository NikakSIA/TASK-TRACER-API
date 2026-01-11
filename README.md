# Task Tracker API

REST API для управления списком задач.  
Проект реализован в учебных целях для изучения backend-разработки,
HTTP-протокола и работы с базой данных.

---

## Стек

- Python
- FastAPI
- SQLite
- Pydantic

---

## Возможности

- Создание задач
- Получение списка задач
- Частичное обновление задач (PATCH)
- Удаление задач
- Фильтрация по статусу выполнения
- Поиск по тексту задачи
- Сортировка по дате создания или названию

---

## Запуск проекта

1. Установить зависимости:
`bash
pip install fastapi uvicorn

2. Запустить сервер:



python -m uvicorn main:app --reload

3. Открыть документацию API:



http://127.0.0.1:8000/docs


---

## Примеры запросов

Получить все задачи:

GET /tasks

Получить только выполненные задачи:

GET /tasks?completed=true

Поиск и сортировка:

GET /tasks?search=home&sort_by=text&order=ASC

Создать задачу:

POST /tasks
{
  "text": "Buy groceries"
}

Обновить задачу:

PATCH /tasks/1
{
  "completed": true
}

Удалить задачу:

DELETE /tasks/1


---

## Что было изучено

Основы HTTP и REST API

Работа с FastAPI

Валидация данных с помощью Pydantic

Работа с SQLite и SQL

Обработка ошибок и HTTP-коды

Проектирование API и работа с query-параметрами
