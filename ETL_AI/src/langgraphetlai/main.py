from src.langgraphetlai.LLMS.groqllm import GroqLLM
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from src.langgraphetlai.nodes.createUserStories import CreateUserStory
from src.langgraphetlai.graph.graphbuilder import GraphBuilder

# MAIN Function START
def load_langgraph_etlai_app():

    initial_input={"messages":HumanMessage(content="The requirement is to transfer employee data file from one directoy to other directory using pyspark")}
    thread={"configurable":{"thread_id":"8"}}

    try:
        obj_llm_config = GroqLLM()
        model = obj_llm_config.get_llm_model()
    
        ### Graph Builder
        graph_builder=GraphBuilder(model)
        graph = graph_builder.setup_graph()

        for event in graph.stream(initial_input,thread,stream_mode="values"):
            event['messages'][-1].pretty_print()

    except Exception as e:
        raise ValueError(f"Error Occurred with Exception : {e}")