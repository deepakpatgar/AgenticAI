from dataclasses import dataclass


@dataclass(frozen=True)
class AgentTask:
    title: str
    status: str = "planned"


def summarize_task(task: AgentTask) -> str:
    return f"Task '{task.title}' is {task.status}."


if __name__ == "__main__":
    sample = AgentTask(title="bootstrap repo")
    print(summarize_task(sample))
