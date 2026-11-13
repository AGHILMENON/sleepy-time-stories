from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.fallback import FALLBACK_STORY
from app.models import StoryRequest
from app.reviewer import review_story
from app.writer import write_story

MAX_ATTEMPTS = 3   # first draft + 2 rewrites


class StoryState(TypedDict, total=False):
    """The shared notebook every step reads and writes."""
    req: StoryRequest
    story: dict
    approved: bool
    fix_notes: str
    attempts: int
    trace: list


def build_graph(writer_llm, reviewer_llm):

    # ---------- nodes (the steps) ----------
    def write(state: StoryState) -> dict:
        story = write_story(writer_llm, state["req"], state.get("fix_notes", ""))
        return {"story": story, "attempts": state.get("attempts", 0) + 1}

    def review(state: StoryState) -> dict:
        req = state["req"]
        result = review_story(reviewer_llm, state["story"]["text"], req.age_band, req.minutes)
        step = {
            "attempt": state["attempts"],
            "word_count": state["story"]["word_count"],
            "safety": result["review"].safety,
            "score": result["review"].total,
            "problems": result["problems"],
            "approved": result["approved"],
        }
        return {
            "approved": result["approved"],
            "fix_notes": result["fix_notes"],
            "trace": state.get("trace", []) + [step],
        }

    def fallback(state: StoryState) -> dict:
        story = {**FALLBACK_STORY, "minutes": state["req"].minutes}
        return {"story": story}

    # ---------- the decision after review ----------
    def route(state: StoryState) -> str:
        if state["approved"]:
            return "done"
        if state["attempts"] < MAX_ATTEMPTS:
            return "retry"
        return "give_up"

    # ---------- wire it together ----------
    graph = StateGraph(StoryState)
    graph.add_node("write", write)
    graph.add_node("review", review)
    graph.add_node("fallback", fallback)

    graph.add_edge(START, "write")
    graph.add_edge("write", "review")
    graph.add_conditional_edges("review", route, {
        "done": END,
        "retry": "write",
        "give_up": "fallback",
    })
    graph.add_edge("fallback", END)

    return graph.compile()


def generate_story(writer_llm, reviewer_llm, req: StoryRequest) -> dict:
    """Same job as before, now run as a LangGraph agent."""
    final = build_graph(writer_llm, reviewer_llm).invoke({"req": req})
    status = "approved" if final.get("approved") else "fallback_used"
    return {**final["story"], "status": status, "attempts": final["attempts"], "trace": final["trace"]}