"""Configuration for SagaAgent workflow."""
import os
import uuid
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class ExportConfig:
    """Export path configuration."""
    EXPORT_DIR: str = "SagaAgent/exports/"
    CHECKPOINT_DB_PATH: str = "SagaAgent/checkpoints.db"


@dataclass
class ModelConfig:
    """Model configuration defaults."""
    DEFAULT_MODEL: str = "gemini-2.0-flash"
    DEFAULT_TEMPERATURE: float = 0.7
    CREATIVE_TEMPERATURE: float = 0.9
    ANALYTICAL_TEMPERATURE: float = 0.3
    MAX_RETRIES: int = int(os.environ.get("MAX_RETRIES", "3"))
    
    @classmethod
    def get_openai_models(cls) -> list[str]:
        """Get list of available OpenAI models from environment or defaults."""
        env_models = os.environ.get("OPENAI_MODELS", "")
        if env_models:
            return [m.strip() for m in env_models.split(",") if m.strip()]
        return [ "gpt-5-mini", "gpt-5-nano", "gpt-4o-mini"]
    
    @classmethod
    def get_google_models(cls) -> list[str]:
        """Get list of available Google models from environment or defaults."""
        env_models = os.environ.get("GOOGLE_MODELS", "")
        if env_models:
            return [m.strip() for m in env_models.split(",") if m.strip()]
        return ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]
    
    @classmethod
    def get_default_openai_model(cls) -> str:
        """Get default OpenAI model."""
        return os.environ.get("DEFAULT_OPENAI_MODEL", cls.DEFAULT_MODEL)
    
    @classmethod
    def get_default_google_model(cls) -> str:
        """Get default Google model."""
        return os.environ.get("DEFAULT_GOOGLE_MODEL", "gemini-2.0-flash")
    
    @classmethod
    def get_default_model(cls) -> str:
        """Get the default model based on available API keys."""
        explicit_model = os.environ.get("MODEL", "").strip()
        if explicit_model:
            return explicit_model
        
        # Auto-select based on available API keys
        if os.environ.get("OPENAI_API_KEY"):
            return cls.get_default_openai_model()
        elif os.environ.get("GOOGLE_API_KEY"):
            return cls.get_default_google_model()
        else:
            return cls.get_default_openai_model()
    
    @property
    def OPENAI_MODELS(self) -> list[str]:
        """OpenAI models list (backward compatibility)"""
        return self.get_openai_models()
    
    @property
    def GOOGLE_MODELS(self) -> list[str]:
        """Google models list (backward compatibility)"""
        return self.get_google_models()


@dataclass
class AgentConfig:
    """Configuration for SagaAgent execution."""
    # Thread and checkpoint management
    thread_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    checkpoint_id: Optional[str] = None
    auto_continue: bool = False
    
    # Model configuration
    model: Optional[str] = None
    model_temperature: Optional[float] = None
    random_seed: Optional[int] = None
    
    # Workflow configuration
    topic: str = ""
    research_summary: Optional[str] = None
    
    # Parallelization settings (enabled by default for 40-50% faster generation)
    parallel_execution: bool = True
    parallel_max_workers: int = 3
    parallel_batch_size: int = 4
    parallel_retry_sequential: bool = True
    
    # Rendering
    enable_render_prep: bool = True
    
    # CLI options
    list_history: bool = False
    verbose: bool = False
    
    @classmethod
    def from_env(cls) -> "AgentConfig":
        """Create config from environment variables."""
        # Parallelization settings (enabled by default)
        parallel_execution = os.environ.get("PARALLEL_EXECUTION", "true").lower() in ("1", "true", "yes", "y")
        parallel_max_workers = int(os.environ.get("PARALLEL_MAX_WORKERS", "3") or 3)
        parallel_batch_size = int(os.environ.get("PARALLEL_BATCH_SIZE", "4") or 4)
        parallel_retry_sequential = os.environ.get("PARALLEL_RETRY_SEQUENTIAL", "true").lower() in ("1", "true", "yes", "y")
        
        return cls(
            thread_id=os.environ.get("THREAD_ID", str(uuid.uuid4())),
            checkpoint_id=os.environ.get("CHECKPOINT_ID"),
            auto_continue=os.environ.get("AUTO_CONTINUE", "false").lower() == "true",
            model=os.environ.get("MODEL"),
            model_temperature=float(t) if (t := os.environ.get("MODEL_TEMPERATURE")) else None,
            random_seed=int(s) if (s := os.environ.get("RANDOM_SEED")) else None,
            topic=os.environ.get("TOPIC", ""),
            research_summary=os.environ.get("RESEARCH_SUMMARY"),
            parallel_execution=parallel_execution,
            parallel_max_workers=parallel_max_workers,
            parallel_batch_size=parallel_batch_size,
            parallel_retry_sequential=parallel_retry_sequential,
            enable_render_prep=os.environ.get("ENABLE_RENDER_PREP", "true").lower() == "true",
            list_history=os.environ.get("LIST_HISTORY", "false").lower() == "true",
            verbose=os.environ.get("VERBOSE", "false").lower() == "true",
        )
    
    def to_state_dict(self) -> dict:
        """Convert config to state dictionary."""
        state = {}
        if self.model:
            state["model"] = self.model
        if self.model_temperature is not None:
            state["model_temperature"] = self.model_temperature
        if self.random_seed is not None:
            state["random_seed"] = self.random_seed
        if self.research_summary:
            state["research_summary"] = self.research_summary
        
        # Parallelization settings
        state["parallel_execution"] = self.parallel_execution
        state["parallel_max_workers"] = self.parallel_max_workers
        state["parallel_batch_size"] = self.parallel_batch_size
        state["parallel_retry_sequential"] = self.parallel_retry_sequential
        
        return state
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)
