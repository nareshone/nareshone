from IPython.display import Image, display
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from src.langgraphetlai.nodes.createUserStories import CreateUserStory
from src.langgraphetlai.nodes.checkSecurity import Code_Security_Feedback
from src.langgraphetlai.nodes.codeGeneration import GenCode
from src.langgraphetlai.nodes.createDesignDocuments import CreateDesignDocs
from src.langgraphetlai.nodes.createTestCases import Create_Test_Cases
from src.langgraphetlai.nodes.executeQATestCases import Execute_QA_Test_Cases

class GraphBuilder:

    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(MessagesState)
        self.memory = MemorySaver()

    def etl_build_graph(self):
        """
        Building graph for ETL process
        """
        self.etl_node=CreateUserStory(self.llm)
        self.etl_node=Code_Security_Feedback(self.llm)
        self.etl_node=GenCode(self.llm)
        self.etl_node=CreateDesignDocs(self.llm)
        self.etl_node=Create_Test_Cases(self.llm)
        self.etl_node=Execute_QA_Test_Cases(self.llm)
        self.etl_node=CreateUserStory(self.llm)
        self.etl_node=CreateUserStory(self.llm)
        self.etl_node=CreateUserStory(self.llm)
        self.etl_node=CreateUserStory(self.llm)
        self.etl_node=CreateUserStory(self.llm)

        self.graph_builder.add_node("writeUserStories",self.etl_node.writeUserStories)
        self.graph_builder.add_node("human_feedback",self.etl_node.human_feedback)
        self.graph_builder.add_edge(START,"writeUserStories")
        self.graph_builder.add_edge("writeUserStories","human_feedback")
        self.graph_builder.add_conditional_edges("human_feedback",self.etl_node.evaluate_feedback,["writeUserStories", END])

    def setup_graph(self):
        """
        Sets up the graph for the selected use case.
        """
        self.etl_build_graph()
        return self.graph_builder.compile(interrupt_before=["human_feedback"],checkpointer=self.memory)
