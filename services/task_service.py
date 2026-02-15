"""Task business logic and event emission."""

from models import Task, TaskStatus
import config
import database
from services import notification_service


def _create_event(category: str, action: str, data: dict) -> dict:
    """Build a structured event payload."""
    return {
        "type": f"{category}.{action}",
        "timestamp": config.get_timestamp(),  # Updated in timezone refactor
        "data": data,
    }


def create_task(title: str, description: str = "") -> dict:
    """Create a new task and emit a creation event."""
    task = Task(
        title=title,
        description=description,
        created_at=config.get_timestamp(),
        updated_at=config.get_timestamp(),
    )
    saved = database.save_task(task.to_dict())

    event = _create_event("task", "created", {"task": saved})
    notification_service.get_instance().handle_event(event)
    return saved


def assign_task(task_id: str, assignee_id: str) -> dict:
    """Assign a task to a user and notify them."""
    task = database.get_task(task_id)
    if task is None:
        raise ValueError(f"Task {task_id} not found")

    task["assignee_id"] = assignee_id
    task["status"] = TaskStatus.IN_PROGRESS.value
    task["updated_at"] = config.get_timestamp()
    database.save_task(task)

    event = _create_event("task", "assigned", {
        "task": task,
        "assignee_id": assignee_id,
    })
    notification_service.get_instance().handle_event(event)
    return task


def complete_task(task_id: str) -> dict:
    """Mark a task as completed."""
    task = database.get_task(task_id)
    if task is None:
        raise ValueError(f"Task {task_id} not found")

    task["status"] = TaskStatus.COMPLETED.value
    task["updated_at"] = config.get_timestamp()
    database.save_task(task)

    event = _create_event("task", "completed", {"task": task})
    notification_service.get_instance().handle_event(event)
    return task


def update_task(task_id: str, **fields) -> dict:
    """Generic field update (title, description, status)."""
    task = database.get_task(task_id)
    if task is None:
        raise ValueError(f"Task {task_id} not found")

    for key in ("title", "description", "status"):
        if key in fields:
            task[key] = fields[key]

    task["updated_at"] = config.get_timestamp()
    return database.save_task(task)
