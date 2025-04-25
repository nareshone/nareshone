from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from src.langgraphetlai.LLMS import GroqLLM
from src.langgraphetlai.state import State
from langgraph.graph import START, StateGraph, END

class Execute_QA_Test_Cases:
    """
    execute the test cases
    """
    def __init__(self,model):
        self.llm = model
    
    def executingTestCases(llm, state: State):
    
        # Checking if 'messages' key exists in 'state'
        if "messages" not in state or not isinstance(state["messages"], dict):
            raise TypeError("State is missing 'messages' or 'messages' is not a valid dictionary.")

        # Check if messages are present, otherwise use default message
        if "messages" in state["messages"] and state["messages"]["messages"]:
            last_message = state["messages"]["messages"][-1].content
        else:
            last_message = "good"  # Default message if no messages are found

        # Checking if 'test_cases_content' and 'code_content' exist in state
        if "test_cases_content" not in state or "code_content" not in state:
            raise ValueError("State is missing 'test_cases_content' or 'code_content'.")
    
        # Preparing the message to execute test cases
        exec_msg = SystemMessage(
            content=f""" You are a QA Tester, execute the below test cases and provide your feedback whether it's good or not. 

            Test Cases: {state["test_cases_content"]}
            Code: {state["code_content"]}
            Feedback: {last_message}
            """
        )
    
        # Ask LLM to execute test cases and provide feedback
        result = llm.invoke([exec_msg])
    
        # Storing the feedback in state
        #state["qa_test_comments"] = result.content
        state["qa_test_comments"] = "its good"  

        return {"messages": [result], "qa_test_comments": result.content}
    
    # Decision function for user stories
    def evaluate_qa_test_feedback(llm, state: State) -> list[str]:
        """Use LLM to classify user feedback as 'positive' or 'negative'."""

        last_message = state["messages"]["messages"][-1].content  

        # System message to guide LLM
        classify_msg = SystemMessage(
            content="Analyze the following feedback and classify it strictly as 'positive' or 'negative'. "
                    "If the feedback suggests dissatisfaction or rewriting the code, classify it as 'negative'. "
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
                return END
    
        return ["GenerateCode"]  # Default if the response is invalid