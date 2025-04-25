from typing import Annotated, Literal, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, List
from langgraph.graph import MessagesState

class State(TypedDict):
    messages: MessagesState
    user_stories: str
    func_document: Annotated[str, "multiple"]  # Allowing multiple values
    tech_document: Annotated[str, "multiple"]  # Allowing multiple values
    code_content: str
    security_comments: str
    test_cases_content: str
    testcases_comments: str
    qa_test_comments: str