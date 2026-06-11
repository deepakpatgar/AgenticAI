from dataclasses import dataclass


@dataclass(frozen=True)
class MealIdea:
    name: str
    effort: str
    ingredients: list[str]


class IdeaAgent:
    def generate(self) -> list[MealIdea]:
        return [
            MealIdea(name="taco bowls", effort="low", ingredients=["rice", "beans", "salsa"]),
            MealIdea(name="pasta primavera", effort="medium", ingredients=["pasta", "vegetables", "olive oil"]),
            MealIdea(name="sheet-pan chicken", effort="medium", ingredients=["chicken", "potatoes", "carrots"]),
        ]


class CriticAgent:
    def choose_best(self, ideas: list[MealIdea]) -> tuple[MealIdea, str]:
        ranked = sorted(ideas, key=lambda idea: (idea.effort != "low", len(idea.ingredients), idea.name))
        best = ranked[0]
        reason = f"selected because {best.name} is the lowest-effort option"
        return best, reason


class SummarizerAgent:
    def summarize(self, idea: MealIdea, reason: str) -> str:
        ingredients = ", ".join(idea.ingredients)
        return f"Best meal: {idea.name} ({idea.effort} effort) with {ingredients}. {reason}."


def run_meal_planner() -> str:
    idea_agent = IdeaAgent()
    critic_agent = CriticAgent()
    summarizer_agent = SummarizerAgent()

    ideas = idea_agent.generate()
    best_idea, reason = critic_agent.choose_best(ideas)
    return summarizer_agent.summarize(best_idea, reason)


if __name__ == "__main__":
    print(run_meal_planner())
