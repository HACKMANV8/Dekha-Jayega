"""LLM service for SagaAgent with structured output support."""
import os
from typing import Type, TypeVar
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from SagaAgent.config import ModelConfig

T = TypeVar('T', bound=BaseModel)


class LLMService:
    """Service for managing LLM interactions - matches ArcueAgent pattern"""
    
    @staticmethod
    def _is_openai_model(model: str) -> bool:
        """Check if the model is an OpenAI model"""
        return model in ModelConfig.get_openai_models()
    
    @staticmethod
    def _is_google_model(model: str) -> bool:
        """Check if the model is a Google model"""
        return model in ModelConfig.get_google_models()
    
    @staticmethod
    def create_llm(
        state: dict,
        creative: bool = False
    ):
        """
        Initialize LLM with appropriate settings.
        
        Args:
            state: Current workflow state containing model configuration
            creative: Whether to use creative temperature settings
            
        Returns:
            Configured LLM instance (ChatOpenAI or ChatGoogleGenerativeAI)
        """
        base_temp = state.get("model_temperature", 0.7)
        temperature = max(base_temp, ModelConfig.CREATIVE_TEMPERATURE) if creative else base_temp
        seed = state.get("random_seed")
        model = state.get("model", ModelConfig.get_default_model())
        
        # Create OpenAI LLM
        if LLMService._is_openai_model(model):
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            if seed is not None:
                return ChatOpenAI(
                    model=model,
                    temperature=temperature,
                    seed=seed,
                    api_key=api_key
                )
            return ChatOpenAI(
                model=model,
                temperature=temperature,
                api_key=api_key
            )
        
        # Create Google LLM
        elif LLMService._is_google_model(model):
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
            if seed is not None:
                return ChatGoogleGenerativeAI(
                    model=model,
                    temperature=temperature,
                    seed=seed,
                    google_api_key=api_key
                )
            return ChatGoogleGenerativeAI(
                model=model,
                temperature=temperature,
                google_api_key=api_key
            )
        
        # Fallback - try to determine provider by checking available API keys
        else:
            print(f"WARNING: Unknown model: {model}. Attempting to use available API key...")
            
            if os.environ.get("OPENAI_API_KEY"):
                fallback_model = ModelConfig.get_default_openai_model()
                print(f"   Using OpenAI fallback: {fallback_model}")
                if seed is not None:
                    return ChatOpenAI(
                        model=fallback_model,
                        temperature=temperature,
                        seed=seed,
                        api_key=os.environ.get("OPENAI_API_KEY")
                    )
                return ChatOpenAI(
                    model=fallback_model,
                    temperature=temperature,
                    api_key=os.environ.get("OPENAI_API_KEY")
                )
            elif os.environ.get("GOOGLE_API_KEY"):
                fallback_model = ModelConfig.get_default_google_model()
                print(f"   Using Google fallback: {fallback_model}")
                if seed is not None:
                    return ChatGoogleGenerativeAI(
                        model=fallback_model,
                        temperature=temperature,
                        seed=seed,
                        google_api_key=os.environ.get("GOOGLE_API_KEY")
                    )
                return ChatGoogleGenerativeAI(
                    model=fallback_model,
                    temperature=temperature,
                    google_api_key=os.environ.get("GOOGLE_API_KEY")
                )
            else:
                raise ValueError("No API keys found. Please set OPENAI_API_KEY or GOOGLE_API_KEY")
    
    @staticmethod
    def create_structured_llm(
        state: dict,
        schema: Type[T],
        creative: bool = False
    ):
        """
        Create LLM with structured output.
        
        Args:
            state: Current workflow state
            schema: Pydantic model for structured output
            creative: Whether to use creative temperature
            
        Returns:
            LLM configured for structured output
        """
        llm = LLMService.create_llm(state, creative=creative)
        return llm.with_structured_output(schema, include_raw=False)
