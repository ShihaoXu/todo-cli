from planner import Task

class TestTask:
    def test_field_access(self):
        task = Task(
            owner="Alice",
            summary="Complete the project",
            status="todo",
            priority="high",
            id=1,
            due_date="2023-10-31",
            tags=["work", "urgent"]
        )
        
        assert task.owner == "Alice"
        assert task.summary == "Complete the project"
        assert task.status == "todo"
        assert task.priority == "high"
        assert task.id == 1
        assert task.due_date == "2023-10-31"
        assert task.tags == ["work", "urgent"]

    def test_task_default(self):
        task = Task()
        
        assert task.owner is None
        assert task.summary is None
        assert task.status is None
        assert task.priority is None
        assert task.id is None
        assert task.due_date is None
        assert task.tags is None

    def test_task_equality(self):
        task1 = Task(
            owner="Alice",
            summary="Complete the project",
            status="todo",
            priority="high",
            id=1,
            due_date="2023-10-31",
            tags=["work", "urgent"]
        )
        
        task2 = Task(
            owner="Alice",
            summary="Complete the project",
            status="todo",
            priority="high",
            id=1,
            due_date="2023-10-31",
            tags=["work", "urgent"]
        )
        
        assert task1 == task2

    def test_task_equality_with_different_id(self):
        task1 = Task(
            owner="Alice",
            summary="Complete the project",
            status="todo",
            priority="high",
            id=1,
            due_date="2023-10-31",
            tags=["work", "urgent"]
        )
        
        task2 = Task(
            owner="Alice",
            summary="Complete the project",
            status="todo",
            priority="high",
            id=2,  # Different ID
            due_date="2023-10-31",
            tags=["work", "urgent"]
        )
        
        assert task1 == task2

    def test_task_from_dict(self):
        task_data = {
            "owner": "Alice",
            "summary": "Complete the project",
            "status": "todo",
            "priority": "high",
            "id": 1,
            "due_date": "2023-10-31",
            "tags": ["work", "urgent"]
        }
        
        task = Task.from_dict(task_data)
        
        assert task.owner == "Alice"
        assert task.summary == "Complete the project"
        assert task.status == "todo"
        assert task.priority == "high"
        assert task.id == 1
        assert task.due_date == "2023-10-31"
        assert task.tags == ["work", "urgent"]

    def test_task_to_dict(self):
        task = Task(
            owner="Alice",
            summary="Complete the project",
            status="todo",
            priority="high",
            id=1,
            due_date="2023-10-31",
            tags=["work", "urgent"]
        )
        
        task_dict = task.to_dict()
        
        assert task_dict["owner"] == "Alice"
        assert task_dict["summary"] == "Complete the project"
        assert task_dict["status"] == "todo"
        assert task_dict["priority"] == "high"
        assert task_dict["id"] == 1
        assert task_dict["due_date"] == "2023-10-31"
        assert task_dict["tags"] == ["work", "urgent"]