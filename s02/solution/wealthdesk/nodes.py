"""
wealthdesk/nodes.py
-------------------
Node functions for the WealthDesk graph.

Session 2 upgrade: respond() uses MessagesState to read and append conversation
messages so the checkpointer can persist them.
"""
from langchain_core.messages import AIMessage, SystemMessage

from .config import SYSTEM_PROMPT
from .state import WealthDeskState
from .tools import llm


# ---------------------------------------------------------------------------
# TODO 2 of 4 -- update respond() to use messages
# ---------------------------------------------------------------------------
# Upgrade respond() so it:
#
#   1. Reads all messages from state, including the current HumanMessage:
#        history = state["messages"]
#
#   2. Builds the LLM input from the system prompt and conversation:
#        messages = [SystemMessage(content=SYSTEM_PROMPT), *history]
#
#   3. Calls the LLM inside a try / except block (same as Session 1).
#
#   4. Returns the assistant reply alongside the response.
#      The incoming HumanMessage is already in the state; MessagesState's
#      reducer appends the returned AIMessage.
#
#   WHY only return the assistant message?
#   The caller supplies the HumanMessage, and MessagesState preserves it.
#
# ---------------------------------------------------------------------------

def respond(state: WealthDeskState) -> dict:
    messages = [SystemMessage(content=SYSTEM_PROMPT), *state["messages"]]

    try:
        result = llm.invoke(messages)
        response_text = result.content
    except Exception as error:
        print(f"[WealthDesk] Error message: {str(error)}")
        response_text = "I'm sorry, but I can't respond right now. Please try again shortly."

    return {
        "response": response_text,
        "messages": [AIMessage(content=response_text)],
    }
