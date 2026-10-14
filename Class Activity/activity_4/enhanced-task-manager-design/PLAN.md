
## 11. ไฟล์ `PLAN.md`

เอกสารนี้เป็นส่วนสำคัญของงาน เพราะโจทย์ต้องการให้แสดงการวางแผนและออกแบบระบบก่อนพัฒนาฟังก์ชันขั้นสูง

```markdown
# Project Plan: Enhanced Task Manager CLI

## 1. Introduction

This document describes the plan for improving a command-line
Task Manager. The project builds on previous iterations by separating
the application into modules and planning tags, search, filtering,
and sorting.

## 2. Project Goals

- Maintain core task-management features.
- Support normal, due-date, and priority tasks.
- Allow tasks to have multiple tags.
- Store tasks persistently in JSON.
- Separate user interface, business logic, data models, and storage.
- Make future enhancements easier to implement and test.

## 3. Requirements

### 3.1 Functional Requirements

1. Users can create normal tasks with descriptions and optional tags.
2. Users can create due-date tasks using YYYY-MM-DD.
3. Users can create priority tasks with High, Medium, or Low priority.
4. Users can list all tasks.
5. Users can mark tasks as completed by ID.
6. Users can delete tasks by ID.
7. The application saves changes to data/tasks.json.
8. The application loads saved tasks on startup.
9. Tasks can have multiple tags.
10. Search will match keywords in task descriptions or tags.
11. Filtering will support status, due date, priority, and tags.
12. Sorting will support ID, due date, and priority.

### 3.2 Non-Functional Requirements

- Usability: The CLI provides clear menus and prompts.
- Reliability: Invalid IDs, dates, and priorities are handled.
- Maintainability: Modules have clear responsibilities.
- Extensibility: New task types and storage methods can be added.
- Performance: Operations should be quick for hundreds of tasks.
- Portability: The application runs with Python 3.10+.

## 4. Scope

### In Scope

- Refactor the application into separate modules.
- Support adding, listing, completing, and deleting tasks.
- Add tags to tasks.
- Persist tasks in JSON.
- Provide placeholders for search, filter, and sort.
- Document architecture and implementation plans.

### Out of Scope

- Full search, filter, and sort implementation.
- GUI or web interface.
- User accounts.
- Reminder notifications.
- Database integration.

## 5. High-Level Architecture

```text
User
 |
 v
main.py
 |
 v
cli_interface.py
 |
 v
task_manager.py
 |              |
 v              v
task.py     data_persistence.py
                    |
                    v
              data/tasks.json
```
