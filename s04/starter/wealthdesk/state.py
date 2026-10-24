"""
wealthdesk/state.py
-------------------
Defines the state that flows through the WealthDesk graph.

Session 4 adds RAG. A new 'retrieved_docs' field carries the policy chunks
fetched by retrieve_docs() into respond(), so the LLM can answer from
BNB's actual documents rather than from training data.
"""
from typing import TypedDict


# ---------------------------------------------------------------------------
# TODO 1 of 4 -- add retrieved_docs to WealthDeskState
# ---------------------------------------------------------------------------
# Add a fifth field to WealthDeskState:
#
#   retrieved_docs: list[str]
#
# Each string in the list is one retrieved policy chunk, formatted as:
#   "[home_loan_guide.md]\n<chunk text here>"
#
# retrieve_docs() populates this field; respond() reads it to build the
# context-augmented system prompt.
#
# The field is cleared at the START of every turn inside classify():
#   return {"query_type": ..., "retrieved_docs": []}
# This prevents stale chunks from a previous question leaking into the
# current answer — the most common RAG defect in production systems.
#
# ---------------------------------------------------------------------------

class WealthDeskState(TypedDict):
    customer_message: str
    response:         str
    history:          list[dict]
    query_type:       str
    # TODO 1: add retrieved_docs field here
