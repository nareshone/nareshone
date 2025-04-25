from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from src.langgraphetlai.LLMS import GroqLLM
from src.langgraphetlai.state import State
from langgraph.graph import START, StateGraph, END

class Create_Test_Cases:
    """
    Generate test cases based on the fuctional and test requirements
    """
    def __init__(self,model):
        self.llm = model

    def writeTestCases(llm, state: State):

        last_message = state['messages']['messages'][-1].content  # Get last human feedback

        # Function to summarize content
        def summarize_content(content, role):
            summary_msg = SystemMessage(
                content=f'Summarize the following {role} document to a concise description, retaining key points for writing test cases.\nContent: {content}'
            )
            summary_response = llm.invoke([summary_msg])
            return summary_response.content.strip()

        # Summarize Functional Design Document
        func_summary = summarize_content(state['func_document'], 'functional design')

        # Summarize Technical Design Document
        tech_summary = summarize_content(state['tech_document'], 'technical design')

        # Summarize Code Content
        code_summary = summarize_content(state['code_content'], 'code')

        # Prepare the test case generation message
        if 'from_test_feedback' in state and state['from_test_feedback'] == True:  
            test_msg = SystemMessage(
                content=f"""
                You are a QA Analyst. Write test cases based on the following summaries of documents and code:

                Functional Design Document Summary: {func_summary}
                Technical Design Document Summary: {tech_summary}
                Code Summary: {code_summary}

                Consider the following feedback: {last_message}
                """
            )
        else:
            test_msg = SystemMessage(
                content=f"""
                You are a QA Analyst. Write test cases based on the following summaries of documents and code:

                Functional Design Document Summary: {func_summary}
                Technical Design Document Summary: {tech_summary}
                Code Summary: {code_summary}
                """
            )

        # Generate test cases
        result = llm.invoke([test_msg])

        # Store the generated test cases
        state['test_cases_content'] = result.content  

        return {'messages': [result], 'test_cases_content': result.content}

    # Decision function for user stories
    def evaluate_test_cases_feedback(llm, state: State) -> list[str]:
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
                return ["writeTestCases"]
            elif decision == "positive":
                return "executingTestCases"
    
        return ["writeTestCases"]  # Default if the response is invalid
    
    # Human feedback node
    def testcases_feedback(state: State):
        return {"messages": state["messages"]}