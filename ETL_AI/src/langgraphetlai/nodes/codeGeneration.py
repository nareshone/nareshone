from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from src.langgraphetlai.LLMS import GroqLLM
from src.langgraphetlai.state import State
from langgraph.graph import START, StateGraph, END

class GenCode:
    """
    Generate code based on the functional and technical documents
    """
    def __init__(self,model):
        self.llm = model
    
    def GenerateCode(llm, state: State):
    
        last_message = state["messages"]["messages"][-1].content  # Get last human input

    # Function to summarize content
        def summarize_content(content, role):
            summary_msg = SystemMessage(
                content=f'Summarize the following {role} document to a concise description, retaining key implementation points.\nContent: {content}'
            )
            summary_response = llm.invoke([summary_msg])
            return summary_response.content.strip()

        # Summarize Functional Design Document
        func_summary = summarize_content(state["func_document"], "functional design")

        # Summarize Technical Design Document
        tech_summary = summarize_content(state["tech_document"], "technical design")

        # Prepare the prompt based on the state flags
        if "from_code_feedback" in state and state["from_code_feedback"] == True:  
            feedback_content = last_message
        elif "from_security_feedback" in state and state["from_security_feedback"] == True:  
            feedback_content = state["security_comments"]
        elif "from_executingTestCases" in state and state["from_executingTestCases"] == True:  
            feedback_content = state["qa_test_comments"]
        else:
            feedback_content = None  # No additional feedback

        # Prepare the generation message
        if feedback_content:
            code_msg = SystemMessage(
                content=f"""
                You are an ETL developer. Generate code based on the following summarized documents:

                Functional Design Document Summary: {func_summary}
                Technical Design Document Summary: {tech_summary}

                Also, consider the following feedback: {feedback_content}
                """
            )
        else:
            code_msg = SystemMessage(
                content=f"""
                You are an ETL developer. Generate code based on the following summarized documents:

                Functional Design Document Summary: {func_summary}
                Technical Design Document Summary: {tech_summary}
                """
            )

        # Generate code
        result = llm.invoke([code_msg])

        # Store the generated code
        state["code_content"] = result.content  

        return {"messages": [result], "code_content": result.content}


        # Decision function for user stories
    def evaluate_code_feedback(llm, state: State) -> list[str]:
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
                return ["security_feedback"]

        return ["GenerateCode"]  # Default if the response is invalid

    # Human feedback node
    def code_feedback(state: State):
        return {"messages": state["messages"]}