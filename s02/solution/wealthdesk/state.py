"""
wealthdesk/state.py
-------------------
Defines the state that flows through the WealthDesk graph.

Session 2 adds multi-turn memory. The checkpointer persists the full state
to SQLite between turns, so messages survive across calls to graph.invoke().
"""
from langgraph.graph import MessagesState


# ---------------------------------------------------------------------------
# TODO 1 of 4 -- add MessagesState to WealthDeskState
# ---------------------------------------------------------------------------
# MessagesState provides the `messages` field with an add_messages reducer.
# WealthDeskState adds the response field consumed by the terminal interface.
#
# The checkpointer saves this list to SQLite after every graph.invoke() call.
# On the next invoke(), LangGraph restores it automatically from the database.
# The respond node reads it to build the full conversation for the LLM.
#
# ---------------------------------------------------------------------------

class WealthDeskState(MessagesState):
    response: str