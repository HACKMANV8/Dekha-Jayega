"""Configuration for RenderPrepAgent."""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class RenderConfig:
    """Configuration for render prep agent."""
    
    # Export paths
    EXPORT_DIR = os.environ.get("RENDER_EXPORT_DIR", "./saga_exports/renders/")
    CHECKPOINT_DB_PATH = os.environ.get("RENDER_CHECKPOINT_DB", "./saga_exports/render_checkpoints.db")
    
    # Image generation settings
    DEFAULT_IMAGE_SIZE = os.environ.get("RENDER_IMAGE_SIZE", "1024x1024")
    DEFAULT_NUM_IMAGES = int(os.environ.get("RENDER_NUM_IMAGES", "1"))
    
    # Nano Banana API settings
    NANO_BANANA_API_KEY = os.environ.get("NANO_BANANA_API_KEY", "")
    NANO_BANANA_ENDPOINT = os.environ.get("NANO_BANANA_ENDPOINT", "https://api.google.com/nano-banana/v1")
    
    # Prompt engineering settings
    USE_PROMPT_WEIGHTING = bool(os.environ.get("RENDER_USE_WEIGHTING", "true").lower() == "true")
    MAX_PROMPT_LENGTH = int(os.environ.get("RENDER_MAX_PROMPT_LENGTH", "500"))
    
    # Quality presets
    QUALITY_PRESETS = {
        "draft": {
            "technical_details": "4K, good focus",
            "render_quality": "standard quality",
            "emphasis_weight": 1.1
        },
        "standard": {
            "technical_details": "8K, sharp focus, professional",
            "render_quality": "high quality, detailed",
            "emphasis_weight": 1.2
        },
        "premium": {
            "technical_details": "8K, ultra detailed, sharp focus, professional photography",
            "render_quality": "ultra high quality, photorealistic, ray tracing",
            "emphasis_weight": 1.3
        }
    }
    
    @classmethod
    def get_quality_preset(cls, preset_name: str = "standard") -> dict:
        """Get quality preset configuration."""
        return cls.QUALITY_PRESETS.get(preset_name, cls.QUALITY_PRESETS["standard"])


class AgentConfig:
    """Agent runtime configuration."""
    
    def __init__(
        self,
        thread_id: str = "render_prep_default",
        auto_continue: bool = True,
        quality_preset: str = "standard",
        generate_images: bool = False,
        model_name: Optional[str] = None,
        model_temperature: float = 0.7,
    ):
        self.thread_id = thread_id
        self.auto_continue = auto_continue
        self.quality_preset = quality_preset
        self.generate_images = generate_images  # Actually call Nano Banana API
        self.model_name = model_name or os.environ.get("RENDER_MODEL", "gemini-2.0-flash-exp")
        self.model_temperature = model_temperature
    
    @classmethod
    def from_env(cls) -> "AgentConfig":
        """Create config from environment variables."""
        return cls(
            thread_id=os.environ.get("RENDER_THREAD_ID", "render_prep_default"),
            auto_continue=os.environ.get("RENDER_AUTO_CONTINUE", "true").lower() == "true",
            quality_preset=os.environ.get("RENDER_QUALITY", "standard"),
            generate_images=os.environ.get("RENDER_GENERATE_IMAGES", "false").lower() == "true",
            model_name=os.environ.get("RENDER_MODEL", "gemini-2.0-flash-exp"),
            model_temperature=float(os.environ.get("RENDER_TEMPERATURE", "0.7")),
        )
    
    def to_state_dict(self) -> dict:
        """Convert config to state dictionary."""
        return {
            "quality_preset": self.quality_preset,
            "generate_images": self.generate_images,
            "model_name": self.model_name,
            "model_temperature": self.model_temperature,
        }

