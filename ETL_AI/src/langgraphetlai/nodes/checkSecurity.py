from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from src.langgraphetlai.LLMS import GroqLLM
from src.langgraphetlai.state import State
from langgraph.graph import START, StateGraph, END

class Code_Security_Feedback:
    """
    It verifies the generated code in terms of security concerns
    """
    def __init__(self,model):
        self.llm = model

    # Decision function for security verification
    def evaluate_security_feedback(llm, state: State) -> list[str]:
        """Use LLM to classify user feedback as 'positive' or 'negative'."""

        last_message = state["messages"]["messages"][-1].content  # Get last human feedback

        # System message to guide LLM
        classify_msg = SystemMessage(
            content="Analyze the following feedback and classify it strictly as 'positive' or 'negative'. "
                    "If the feedback suggests dissatisfaction or rewriting, classify it as 'negative'. "
                    "Otherwise, classify it as 'positive'. Return only 'positive' or 'negative' as output.\n"
                    f"Feedback: {last_message}"
        )

        # Ask LLM to classify
        response = llm.invoke([classify_msg])

        if hasattr(response, 'content') and response.content:
            decision = response.content.strip().lower()
            print(f"Decision made by evaluator: {decision}")  # Log decision
            if decision == "negative":
                return ["GenerateCode"]
            elif decision == "positive":
                return ["writeTestCases"]
    
        return ["GenerateCode"]  # Default if the response is invalid

    # Human feedback node
    def security_feedback(state: State):
        return {"messages": state["messages"]}