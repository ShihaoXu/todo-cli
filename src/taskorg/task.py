from dataclasses import asdict, dataclass, field

# We are using str for priority and status types to simplify (de-)serialization.
def is_valid_priority(val: str) -> bool:
    return True if val.lower() in ['low', 'medium', 'high'] else False
def priority_rank(val: str) -> int:
    """Return the rank of the priority."""
    if not is_valid_priority(val):
        raise PrioException(f"Invalid priority value: {val}")
    rank = {'low': 0, 'medium': 1, 'high': 2}
    return rank[val]


def is_valid_status(val: str):
    return True if val.lower() in ['todo', 'in_progress', 'done'] else False
def status_rank(val: str) -> int:
    """Return the rank of the status."""
    if not is_valid_status(val):
        raise StatusException(f"Invalid status value: {val}")
    rank = {'todo': 2, 'in_progress': 1, 'done': 0}
    return rank[val]

@dataclass
class Task:
    owner: str | None = None
    summary: str | None = None
    status: str | None = None
    priority: str | None = None
    id: int | None = field(default=None, compare=False)
    due_date: str | None = None # default_factory=lambda: date.today().strftime("%Y-%m-%d")
    tags: list[str] | None = None# field(default_factory=list)

    UPDATE_PROPERTIES = ["owner", "summary", "priority", "due_date", "tags"]
    SORT_PROPERTIES = ["owner", "status", "priority", "due_date"]
    
    @classmethod
    def from_dict(cls, d):
        if (prio := getattr(d, "priority", None)) is not None and not is_valid_priority(prio):
            raise PrioException(f"Invalid priority value: {prio}")
        if (status := getattr(d, "status", None)) is not None and not is_valid_status(status):
            raise StatusException(f"Invalid status value: {status}")
        return Task(**d)

    def to_dict(self):
        return asdict(self) # Note that StrEnum loses its type when serialized

class TaskException(Exception):
    """Base class for task-related exceptions."""

class PrioException(TaskException):
    """Raised when an invalid priority is encountered."""

class StatusException(TaskException):
    """Raised when an invalid status is encountered."""

class InvalidTaskId(TaskException):
    """Raised when a task ID is invalid."""

class InvalidOwner(TaskException):
    """Raised when an owner is invalid."""

class MissingSummary(TaskException):
    """Raised when a task summary is missing."""
