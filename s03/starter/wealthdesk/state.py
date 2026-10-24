"""
wealthdesk/state.py
-------------------
Defines the state that flows through the WealthDesk graph.

Session 3 adds query routing. A new 'query_type' field records the
classification result from classify() so route_query() can read it
and direct the graph to the right terminal node.
"""
from typing import TypedDict


# ---------------------------------------------------------------------------
# TODO 1 of 4 -- add query_type to WealthDeskState
# ---------------------------------------------------------------------------
# Add a fourth field to WealthDeskState:
#
#   query_type: str
#
# This field is written by classify() and read by route_query().
# Valid values: "SIMPLE", "COMPLEX", "OUT_OF_SCOPE"
#
# The checkpointer saves this field to SQLite along with everything else,
# so if you inspect the state after a run you can see which path was taken.
# It is overwritten on every new turn -- it always reflects the classification
# of the CURRENT question, not any previous one.
#
# ---------------------------------------------------------------------------

class WealthDeskState(TypedDict):
    customer_message: str
    response:         str
    history:          list[dict]
    # TODO 1: add query_type field here
