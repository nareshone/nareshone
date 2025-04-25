from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from src.langgraphetlai.LLMS import GroqLLM
from src.langgraphetlai.state import State
from langgraph.graph import START, StateGraph, END
class CreateUserStory:
    """
    Create user story based on the requiremments
    """
    def __init__(self,model):
        self.llm = model

    def writeUserStories(llm, state: State):
    
        last_message = state["messages"]["messages"][-1].content  # Get last human input

        # System message to guide LLM for classification
        classify_msg = SystemMessage(
            content=f"""
            You are a classifier. Your task is to strictly classify the given message as 'requirement' or 'feedback'. 
            If the message suggests dissatisfaction, suggests improvements, or requests rewriting of user stories, 
            classify it as 'feedback'. Otherwise, classify it as 'requirement'.
        
            Return only the word 'requirement' or 'feedback'. 
        
            Message to classify: {last_message}
            """
        )
        print(classify_msg)  # Debugging print

        # Ask LLM to classify
        response = llm.invoke([classify_msg])
    
        if hasattr(response, 'content') and response.content.strip().lower() == 'feedback':
            # Rewrite if it's feedback
            rewrite_msg = SystemMessage(
                content=f"As you are a business analyst, Rewrite the user stories based on the feedback provided: {last_message}"
            )
            result = llm.invoke([rewrite_msg] + state["messages"]["messages"])
        
        else:
            # Process the requirement
            sys_msg = SystemMessage(content="You are the business analyst and your job is to create user stories based on the requirements")
            result = llm.invoke([sys_msg] + state["messages"]["messages"])
    
    
        # Append the latest user story to the list
        state["user_stories"] = result.content  

        return {"messages": [result], "user_stories": result.content}


    # Human feedback node
    def po_feedback(state: State):
        return {"messages": state["messages"]}

    
    # Decision function for user stories
    def evaluate_feedback(llm, state: State) -> list[str]:
        """Use LLM to classify user feedback as 'positive' or 'negative'."""

        last_message = state["messages"]["messages"][-1].content  # Get last human feedback
        print("last_message====>"+last_message)

        #  System message to guide LLM
        classify_msg = SystemMessage(
            content="Analyze the following feedback and classify it strictly as 'positive' or 'negative'. "
                    "If the feedback suggests dissatisfaction, or rewriting, classify it as 'negative'. "
                    "Otherwise, classify it as 'positive'. Return only 'positive' or 'negative' as output.\n"
                    f"Feedback: {last_message}"
        )

        # Ask LLM to classify
        response = llm.invoke([classify_msg])

        if hasattr(response, 'content') and response.content:
            decision = response.content.strip().lower()
            print(f"Decision made by evaluator: {decision}")  # Log decision
            if decision == "negative":
                return ["writeUserStories"]
            elif decision == "positive":
                return ["createFuncDesignDocument", "createTechDesignDocument"]
        print("Defaulting to writeUserStories due to unexpected decision.")  # Log fallback case
        return ["writeUserStories"]  # Default if the response is invalid