"""
wealthdesk/state.py
-------------------
Defines the state that flows through the WealthDesk graph.

Session 2 adds multi-turn memory. The checkpointer persists the full state
to SQLite between turns, so history survives across calls to graph.invoke().
"""
from typing import TypedDict


# ---------------------------------------------------------------------------
# TODO 1 of 4 -- add history to WealthDeskState
# ---------------------------------------------------------------------------
# Add a third field to WealthDeskState:
#
#   history: list[dict]
#
# Each dict in the list represents one conversation turn:
#   {"role": "user",      "content": "What is the home loan rate?"}
#   {"role": "assistant", "content": "The home loan rate starts at 8.5%..."}
#
# The checkpointer saves this list to SQLite after every graph.invoke() call.
# On the next invoke(), LangGraph restores it automatically from the database.
# The respond node reads it to build the full conversation for the LLM.
#
# ---------------------------------------------------------------------------

class WealthDeskState(TypedDict):
    customer_message: str
    response:         str
    # TODO 1: add history field here
