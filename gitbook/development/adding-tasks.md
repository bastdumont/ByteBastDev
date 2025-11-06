# Adding New Task Types

Steps to introduce a new task category.

## 1) Extend Enum

- Add value to TaskType in `task_planner.py`

## 2) Add Engine Handler

- Implement `_execute_<type>` in `execution_engine.py`

## 3) Route in Dispatcher

- Update `execute_task()` to call your handler

## 4) Generate Tasks

- Add rules in `TaskPlanner._generate_tasks()`

## 5) Tests & Docs

- Add unit tests and update GitBook references


