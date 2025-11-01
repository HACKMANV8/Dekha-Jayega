import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from ArcueAgent.config import ModelConfig

load_dotenv()

class OpenAILLM:
    """LLM provider for Research agent with support for OpenAI and Google models"""
    
    def get_llm_model(self):
        """
        Get the main LLM model for research.
        Priority: RESEARCH_MODEL env var > OPENAI_API_KEY > GOOGLE_API_KEY
        Uses ModelConfig for default model selection.
        """
        # Check for explicit RESEARCH_MODEL env var
        research_model = os.environ.get("RESEARCH_MODEL")
        
        if research_model:
            if "gpt" in research_model.lower() or "openai" in research_model.lower():
                return ChatOpenAI(
                    model=research_model,
                    api_key=os.environ.get("OPENAI_API_KEY")
                )
            else:
                return ChatGoogleGenerativeAI(
                    model=research_model,
                    google_api_key=os.environ.get("GOOGLE_API_KEY")
                )
        
        # Auto-select based on available API keys using ModelConfig
        if os.environ.get("OPENAI_API_KEY"):
            return ChatOpenAI(
                model=ModelConfig.get_default_openai_model(),
                api_key=os.environ.get("OPENAI_API_KEY")
            )
        elif os.environ.get("GOOGLE_API_KEY"):
            return ChatGoogleGenerativeAI(
                model=ModelConfig.get_default_google_model(),
                google_api_key=os.environ.get("GOOGLE_API_KEY")
            )
        else:
            raise ValueError("No API keys found. Please set OPENAI_API_KEY or GOOGLE_API_KEY")

    def get_evaluator_model(self):
        """
        Get the evaluator model for research quality assessment.
        Priority: RESEARCH_EVALUATOR_MODEL env var > same as main research model
        Uses ModelConfig for default model selection.
        """
        evaluator_model = os.environ.get("RESEARCH_EVALUATOR_MODEL")
        
        if evaluator_model:
            if "gpt" in evaluator_model.lower() or "openai" in evaluator_model.lower():
                return ChatOpenAI(
                    model=evaluator_model,
                    api_key=os.environ.get("OPENAI_API_KEY")
                )
            else:
                return ChatGoogleGenerativeAI(
                    model=evaluator_model,
                    google_api_key=os.environ.get("GOOGLE_API_KEY")
                )
        
        # Use same model as main research model
        return self.get_llm_model()