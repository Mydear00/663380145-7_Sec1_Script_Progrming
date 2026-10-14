
# Project Plan: Enhanced Task Manager CLI

## 1. Introduction

This document describes the plan for enhancing a command-line Task Manager.
The project builds on previous iterations by separating the application into
modules and implementing tags, search, filtering, and sorting.

The goal is to provide a modular, reliable, and user-friendly command-line
application that supports task management and efficient task organization.

## 2. Project Goals

- Maintain core task-management features.
- Support normal, due-date, and priority tasks.
- Allow tasks to have multiple tags.
- Store tasks persistently in JSON.
- Separate user interface, business logic, data models, and storage.
- Implement functional search, filtering, and sorting.
- Handle invalid user input without unexpectedly terminating the application.
- Make future enhancements easier to implement and test.

## 3. Requirements

### 3.1 Functional Requirements

1. Users can create normal tasks with descriptions and optional tags.
2. Users can create due-date tasks using the `YYYY-MM-DD` format.
3. Users can create priority tasks with High, Medium, or Low priority.
4. Users can list all tasks.
5. Users can mark tasks as completed by ID.
6. Users can delete tasks by ID.
7. The application saves task changes to `data/tasks.json`.
8. The application loads saved tasks on startup.
9. Tasks can have multiple tags.
10. Users can add tags to existing tasks.
11. Users can remove tags from existing tasks.
12. Search matches keywords in task descriptions or tags without
    being case-sensitive.
13. Filtering supports task status, due-date conditions, priority, and tags.
14. Users can combine multiple filter conditions in a single search.
15. Sorting supports task ID, description, completion status, due date,
    and priority.
16. Sorting supports ascending and descending order.
17. Tasks without a due date or priority are handled consistently when sorting.
18. Search, filter, and sort display matching or ordered results clearly.
19. Invalid search, filter, and sort input is handled with helpful messages.
20. Search, filter, and sort do not unintentionally modify or delete stored tasks.

### 3.2 Non-Functional Requirements

- **Usability:** The CLI provides clear menus, prompts, and result messages.
- **Reliability:** Invalid IDs, dates, priorities, and filter criteria are handled.
- **Maintainability:** Modules have clear and separate responsibilities.
- **Extensibility:** New task types and storage methods can be added.
- **Performance:** Operations should be efficient for hundreds of tasks.
- **Portability:** The application runs with Python 3.10 or later.
- **Data Integrity:** Existing tasks remain intact during search, filtering,
  sorting, and application restarts.
- **Testability:** Core task-management operations can be verified with tests.

## 4. Scope

### In Scope

- Refactor the application into separate modules.
- Support adding, listing, completing, and deleting tasks.
- Support normal, due-date, and priority task types.
- Add and remove tags from tasks.
- Persist tasks in JSON.
- Implement keyword search across task descriptions and tags.
- Implement filtering by status, due date, priority, and tags.
- Support combining multiple filter criteria.
- Implement sorting by ID, description, completion status, due date,
  and priority.
- Support ascending and descending sorting.
- Handle invalid input and empty search results.
- Test search, filtering, sorting, and existing task-management functions.
- Document the architecture, implementation, testing, and future work.

### Out of Scope

- Graphical user interface or web interface.
- User accounts and authentication.
- Reminder notifications.
- Database integration.
- Cloud synchronization.
- Multi-user collaboration.

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
 |             |
 v             v
task.py    data_persistence.py
                  |
                  v
            data/tasks.json
```

### Module Responsibilities

- **main.py:** Initializes the application and starts the CLI.
- **cli_interface.py:** Displays menus, receives input, and presents results.
- **task_manager.py:** Implements task operations, search, filtering, and sorting.
- **task.py:** Defines task models, task attributes, and tag operations.
- **data_persistence.py:** Loads and saves tasks in JSON format.
- **data/tasks.json:** Stores task data between application runs.

## 6. Implementation Plan

### Phase 1: Project Structure

- Separate the application into modules.
- Confirm that the main program can start successfully.
- Verify that existing task-management features continue to work.

### Phase 2: Task Models and Tags

- Support normal, due-date, and priority tasks.
- Support multiple tags per task.
- Implement adding and removing tags.
- Verify that task data can be serialized and restored.

### Phase 3: JSON Persistence

- Load saved tasks when the application starts.
- Save task changes to `data/tasks.json`.
- Preserve the correct task type when loading saved data.
- Verify that data remains available after restarting the application.

### Phase 4: Search

- Search task descriptions and tags by keyword.
- Ignore differences between uppercase and lowercase letters.
- Handle blank search input and cases with no matches.
- Display the matching tasks clearly.

### Phase 5: Filtering

- Filter tasks by Pending or Completed status.
- Filter tasks by due-date conditions.
- Filter tasks by High, Medium, or Low priority.
- Filter tasks by tags.
- Allow users to combine supported criteria.
- Display a helpful message when no tasks match the conditions.

### Phase 6: Sorting

- Sort tasks by ID.
- Sort tasks by description.
- Sort tasks by completion status.
- Sort tasks by due date.
- Sort tasks by priority.
- Support ascending and descending order.
- Handle tasks without due dates or priorities consistently.

### Phase 7: Testing and Validation

- Test normal, due-date, and priority task creation.
- Test adding, listing, completing, and deleting tasks.
- Test adding and removing tags.
- Test search with matching and non-matching keywords.
- Test filters individually and in combination.
- Test sorting with different fields and directions.
- Test invalid dates, priorities, and filter values.
- Test JSON persistence after restarting the application.
- Verify that search, filtering, and sorting do not alter stored tasks.

### Phase 8: Documentation and Final Review

- Update the README with setup and usage instructions.
- Document implemented features and known limitations.
- Run the application from the project directory.
- Review the code structure and error handling.
- Prepare a demonstration of the completed features.

## 7. Acceptance Criteria

The project is considered complete when:

1. All existing core task-management features work correctly.
2. Tasks support tags and preserve their data in JSON.
3. Search returns tasks matching descriptions or tags.
4. Filtering returns tasks matching the selected conditions.
5. Multiple filter conditions can be combined.
6. Sorting orders tasks correctly by each supported field.
7. Ascending and descending sorting work as expected.
8. Invalid input does not unexpectedly terminate the application.
9. Empty results are communicated clearly to the user.
10. Existing task data remains intact after normal operations and restarts.
11. The application runs on Python 3.10 or later.
12. Tests confirm the expected behavior of the implemented features.

## 8. Risks and Mitigation

- **Invalid user input:** Validate dates, priorities, and filter criteria.
- **Incorrect sorting:** Define consistent ordering for missing dates and priorities.
- **Data loss:** Test JSON loading and saving before and after modifications.
- **Regression:** Retest existing task-management features after enhancements.
- **Unexpected empty results:** Display a clear message when no tasks match.

## 9. Future Enhancements

- Add task categories and advanced search options.
- Support CSV export and import.
- Add task deadlines and overdue indicators.
- Introduce automated tests for additional edge cases.
- Consider database storage for larger task collections.
