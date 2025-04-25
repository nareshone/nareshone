from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from src.langgraphetlai.LLMS import GroqLLM
from src.langgraphetlai.state import State
from langgraph.graph import START, StateGraph, END

class CreateDesignDocs:
    """
    Create functional and design documents based on the requiremments
    """
    def __init__(self,model):
        self.llm = model

    def createFuncDesignDocument(llm, state: State):
    
        last_message = state["messages"]["messages"][-1].content  # Get last human input

        # Check if the last message came from design_feedback by using a flag in state
        if "from_design_feedback" in state and state["from_design_feedback"] == True:  
            func_msg = SystemMessage(
                content=f""" You are an ETL developer, create a functional design document based on these user stories: {state["user_stories"]}.
                Also, consider the following feedback: {last_message}
                """
            )
        else:
            func_msg = SystemMessage(
                content=f""" You are an ETL developer, create a functional design document based on these user stories: {state["user_stories"]}."""
            )
    

        # Ask LLM to classify
        result = llm.invoke([func_msg] + state["messages"]["messages"])
    
        # Append the latest functional document to the list
        state["func_document"] = result.content  

        return {"messages": [result], "func_document": result.content}

    def createTechDesignDocument(llm, state: State):
    
        last_message = state["messages"]["messages"][-1].content  # Get last human input

        # Check if the last message came from design_feedback by using a flag in state
        if "from_design_feedback" in state and state["from_design_feedback"] == True:  
            tech_msg = SystemMessage(
                content=f""" You are an ETL developer, create a technical design document based on these user stories: {state["user_stories"]}.
                Also, consider the following feedback: {last_message}
                """
            )
        else:
            tech_msg = SystemMessage(
                content=f""" You are an ETL developer, create a technical design document based on these user stories: {state["user_stories"]}."""
            )
    

        # Ask LLM to classify
        result = llm.invoke([tech_msg] + state["messages"]["messages"])
    
        # Append the latest functional document to the list
        state["tech_document"] = result.content  

        return {"tech_document": result.content}

    # Decision function for user stories
    def evaluate_feedback_design(llm, state: State) -> list[str]:
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
                return ["createFuncDesignDocument","createTechDesignDocument"]
            elif decision == "positive":
                return ["GenerateCode"]
    
        return ["writeUserStories"]  # Default if the response is invalid
    
    # Human feedback node
    def design_feedback(state: State):
        return {"messages": state["messages"]}