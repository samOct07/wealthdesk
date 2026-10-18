"""
wealthdesk/agent.py
-------------------
Graph construction and the terminal loop.

Run the agent from the repo root:
    cd cohort-1/wealthdesk/s02/starter
    python -m wealthdesk.agent

Session 2 graph:
    START --> respond --> END   (same topology as S01)

What is new in Session 2:
  - build_graph() accepts an optional checkpointer so callers can choose
    how state is persisted (SQLite for the terminal app, None for Studio).
  - run() creates a SqliteSaver and passes a thread_id so the checkpointer
    can store and restore history across turns.
"""
import sqlite3
from uuid import uuid4

# If you see "AttributeError: JsonPlusSerializer has no attribute dumps", run:
#   pip install "langgraph-checkpoint-sqlite>=3.0.0,<4.0"
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from .config import CHECKPOINT_DB
from .nodes import respond
from .state import WealthDeskState


# ---------------------------------------------------------------------------
# How the checkpointer works
# ---------------------------------------------------------------------------
# The checkpointer is LangGraph's persistence layer. It saves the entire
# WealthDeskState (all fields including history) to SQLite after every
# graph.invoke() call, and restores it before the next one.
#
# Turn 1: checkpointer finds nothing for this thread_id → starts fresh
#         respond() runs → returns updated history
#         checkpointer SAVES full state to SQLite
#
# Turn 2: checkpointer finds Turn 1 state → RESTORES it into WealthDeskState
#         respond() runs with history already populated → LLM sees full context
#         checkpointer SAVES updated state to SQLite
#
# state.py declares WHAT exists (the schema).
# The checkpointer handles WHERE it lives between turns (SQLite).
# You need both: without the declaration LangGraph rejects the field;
# without the checkpointer history vanishes after every invoke().
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# TODO 3 of 4 -- update build_graph() to accept a checkpointer
# ---------------------------------------------------------------------------
# Change the signature so callers can pass in a checkpointer:
#
#   def build_graph(checkpointer=None):
#
# Then pass it straight to compile():
#
#   return builder.compile(checkpointer=checkpointer)
#
# WHY None as the default?
# The module-level `graph = build_graph()` below must have NO checkpointer.
# LangGraph Studio rejects graphs that have one attached. Callers that need
# persistence (like run() below) pass their own checkpointer explicitly.
#
# The rest of build_graph() is identical to Session 1:
#   builder = StateGraph(WealthDeskState)
#   builder.add_node("respond", respond)
#   builder.add_edge(START, "respond")
#   builder.add_edge("respond", END)
#
# ---------------------------------------------------------------------------

def build_graph(checkpointer=None):
    """Build and compile the WealthDesk LangGraph graph."""
    raise NotImplementedError("TODO 3: implement build_graph() with checkpointer in wealthdesk/agent.py")


# Module-level graph instance required by langgraph.json for LangGraph Studio.
graph = build_graph()


# ---------------------------------------------------------------------------
# TODO 4 of 4 -- wire up SqliteSaver and thread_id in run()
# ---------------------------------------------------------------------------
# Three things to add inside run():
#
#   1. Open the SQLite connection and build the graph with a checkpointer:
#        conn   = sqlite3.connect(str(CHECKPOINT_DB), check_same_thread=False)
#        _graph = build_graph(checkpointer=SqliteSaver(conn))
#
#   2. Create a unique thread_id for this session and wrap it in a config dict:
#        thread_id = str(uuid4())
#        config    = {"configurable": {"thread_id": thread_id}}
#
#      The checkpointer uses thread_id as the key to store and retrieve state.
#      Every call to graph.invoke() with the same thread_id continues the same
#      conversation. A new uuid4() starts a fresh one.
#
#   3. Pass config to every graph.invoke() call:
#        result = _graph.invoke(
#            {"customer_message": user_input, "response": ""},
#            config=config,
#        )
#
#      Notice there is no "history" key in the input dict. The checkpointer
#      restores it automatically from the database before the node runs.
#
# ---------------------------------------------------------------------------

def run() -> None:
    # TODO 4: open SQLite connection and build graph with SqliteSaver
    # TODO 4: create thread_id and config dict

    print("=" * 55)
    print("  WealthDesk | Bharat National Bank")
    print("  Type 'quit' to exit")
    print("=" * 55)
    # TODO 4: print the first 8 chars of thread_id here so you can confirm
    #         the session id in the terminal output
    print("=" * 55)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nWealthDesk: Session ended. Goodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit", "bye"}:
            print("\nWealthDesk: Thank you for choosing Bharat National Bank. Goodbye!")
            break

        # TODO 4: invoke _graph with config instead of graph without config
        result = graph.invoke({"customer_message": user_input, "response": ""})
        print(f"\nWealthDesk: {result['response']}")


if __name__ == "__main__":
    run()
