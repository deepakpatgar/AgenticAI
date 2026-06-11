from __future__ import annotations

import warnings
from typing import TypedDict

from langchain_core.prompts import ChatPromptTemplate


warnings.filterwarnings(
    "ignore",
    category=PendingDeprecationWarning,
    module=r"langgraph\.checkpoint\.base",
)

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict, total=False):
    goal: str
    candidate_ideas: list[str]
    best_idea: str
    report: str
    trace: list[str]


def _append_trace(state: AgentState, note: str) -> list[str]:
    return [*state.get("trace", []), note]


def planning_agent(state: AgentState) -> AgentState:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a planning agent that proposes concise candidate ideas."),
            ("human", "Goal: {goal}"),
        ]
    )
    rendered_prompt = prompt.format(goal=state["goal"])

    ideas = [
        "Build a two-agent meal planner that proposes and critiques dinners.",
        "Create a hotel concierge agent that recommends rooms, dining, and add-ons.",
        "Assemble a study coach agent that turns a goal into a daily plan.",
    ]

    return {
        "candidate_ideas": ideas,
        "trace": _append_trace(
            state,
            f"Planning agent prompt:\n{rendered_prompt}\nPlanning agent generated {len(ideas)} ideas.",
        ),
    }


def critic_agent(state: AgentState) -> AgentState:
    ideas = state.get("candidate_ideas", [])
    best_idea = ideas[0] if ideas else "Build a simple agent demo."
    return {
        "best_idea": best_idea,
        "trace": _append_trace(state, f"Critic agent selected: {best_idea}"),
    }


def presenter_agent(state: AgentState) -> AgentState:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a presenter agent that turns a decision into a short demo summary."),
            ("human", "Goal: {goal}\nChosen idea: {best_idea}"),
        ]
    )
    rendered_prompt = prompt.format(goal=state["goal"], best_idea=state["best_idea"])
    report = (
        "LangChain and LangGraph demo\n"
        f"Goal: {state['goal']}\n"
        f"Chosen idea: {state['best_idea']}\n\n"
        "Why this is a useful pattern: LangChain handles prompt construction, while LangGraph\n"
        "orchestrates the agents as a graph so each step can add state and hand off to the next one."
    )
    return {
        "report": report,
        "trace": _append_trace(state, f"Presenter agent prompt:\n{rendered_prompt}\nPresenter agent finalized the report."),
    }


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("planner", planning_agent)
    graph.add_node("critic", critic_agent)
    graph.add_node("presenter", presenter_agent)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "critic")
    graph.add_edge("critic", "presenter")
    graph.add_edge("presenter", END)
    return graph.compile()


def run_demo(goal: str = "Show a practical agent workflow") -> AgentState:
    app = build_graph()
    return app.invoke({"goal": goal, "trace": []})


if __name__ == "__main__":
    result = run_demo()
    print(result["report"])
    print()
    print("Trace:")
    for step in result.get("trace", []):
        print(f"- {step}")