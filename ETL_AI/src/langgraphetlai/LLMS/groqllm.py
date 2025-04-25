import os
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv


class GroqLLM:

    def get_llm_model(self):
        try:
            load_dotenv()
            os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
            llm=ChatGroq(model="qwen-2.5-32b")

        except Exception as e:
            raise ValueError(f"Error Occurred with Exception : {e}")
        return llm