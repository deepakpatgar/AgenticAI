from dataclasses import dataclass


@dataclass(frozen=True)
class AgentTask:
    title: str
    status: str = "planned"
    owner: str = "unassigned"


def summarize_task(task: AgentTask) -> str:
    return f"Task '{task.title}' is {task.status} and owned by {task.owner}."


def render_overview(tasks: list[AgentTask]) -> str:
    lines = ["Agent task overview:"]
    for task in tasks:
        lines.append(f"- {task.title} ({task.status}) -> {task.owner}")
    return "\n".join(lines)


if __name__ == "__main__":
    sample = AgentTask(title="bootstrap repo")
    next_task = AgentTask(title="wire git demo", status="in progress", owner="deepa")
    print(summarize_task(sample))
    print(render_overview([sample, next_task]))
