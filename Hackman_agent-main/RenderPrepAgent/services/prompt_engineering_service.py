"""
Prompt Engineering Service implementing techniques from GUIDE.md and README.md.

This service transforms narrative descriptions into optimized image generation prompts
with proper weighting, negative prompts, and structured formatting.
"""
from typing import Dict, List, Optional, Any
import re


class PromptEngineeringService:
    """
    Professional prompt engineering for AI image generation.
    
    Implements techniques from:
    - Prompt weighting/emphasis (parentheses method)
    - Negative prompt generation
    - Structured syntax: [Image Type] of [Subject] + [Action], [Setting], [Style], [Lighting], [Technical]
    """
    
    # === Common Negative Prompts ===
    NEGATIVE_ANATOMY = [
        "extra limbs", "extra fingers", "missing fingers", "poorly drawn hands",
        "bad anatomy", "extra arms", "fused fingers", "malformed limbs",
        "poorly drawn face", "distorted eyes", "asymmetrical features"
    ]
    
    NEGATIVE_QUALITY = [
        "blurry", "low quality", "low resolution", "worst quality", "grainy",
        "pixelated", "jpeg artifacts", "out of focus", "bad composition"
    ]
    
    NEGATIVE_UNWANTED = [
        "watermark", "signature", "text", "logo", "username",
        "duplicate", "cropped", "out of frame"
    ]
    
    # === Art Styles ===
    ART_STYLES = {
        "fantasy": "fantasy art, concept art style, painterly, epic",
        "realistic": "photorealistic, cinematic, professional photography",
        "anime": "anime style, manga, cel shaded, vibrant colors",
        "painterly": "digital painting, painterly style, artistic",
        "illustration": "illustration, concept art, detailed artwork",
        "3d": "3D render, CGI, octane render, physically based rendering",
        "stylized": "stylized art, game art, modern illustration",
        "pixel_art": "pixel art, retro gaming, 16-bit style",
        "watercolor": "watercolor painting, soft colors, traditional media",
        "comic": "comic book style, ink outlines, dramatic shading"
    }
    
    # === Lighting Presets ===
    LIGHTING_PRESETS = {
        "dramatic": "dramatic lighting, hard light, chiaroscuro, rim light",
        "soft": "soft lighting, diffused light, gentle illumination",
        "natural": "natural lighting, golden hour, soft shadows",
        "studio": "studio lighting, three-point lighting, professional setup",
        "atmospheric": "volumetric lighting, atmospheric fog, god rays",
        "backlit": "backlit, rim lighting, glowing edges",
        "night": "night scene, moonlight, ambient darkness",
        "magical": "magical glow, ethereal light, bioluminescent"
    }
    
    @staticmethod
    def apply_emphasis(text: str, weight: float = 1.2) -> str:
        """
        Apply emphasis weighting to text using parentheses method.
        
        Weight mapping:
        - 1.1x = (word)
        - 1.2x = ((word))
        - 1.3x = (((word)))
        - 1.4x = ((((word))))
        
        Args:
            text: Text to emphasize
            weight: Weight multiplier (1.1-1.4)
        
        Returns:
            Emphasized text with parentheses
        """
        if weight <= 1.0:
            return text
        
        # Determine number of parentheses based on weight
        if weight >= 1.4:
            parens = 4
        elif weight >= 1.3:
            parens = 3
        elif weight >= 1.2:
            parens = 2
        else:
            parens = 1
        
        return f"{'(' * parens}{text}{')' * parens}"
    
    @staticmethod
    def apply_numeric_weight(text: str, weight: float) -> str:
        """
        Apply numeric weighting using bracket syntax: [word:1.2]
        
        Args:
            text: Text to weight
            weight: Weight value
        
        Returns:
            Weighted text with brackets
        """
        return f"({text}:{weight})"
    
    @classmethod
    def build_character_prompt(
        cls,
        character_name: str,
        character_type: str,
        appearance: str,
        art_style: str,
        pose: str = "",
        color_palette: str = "",
        quality_preset: Dict[str, Any] = None,
        additional_details: Dict[str, str] = None
    ) -> Dict[str, str]:
        """
        Build optimized character portrait prompt.
        
        Syntax: [Image Type] of [Subject] + [Action], [Setting], [Style], [Lighting], [Technical]
        
        Args:
            character_name: Name of the character
            character_type: Type (Protagonist, Companion, NPC, Villain, etc.)
            appearance: Detailed visual description
            art_style: Art style keyword (fantasy, realistic, anime, etc.)
            pose: Suggested pose or stance
            color_palette: Color palette description
            quality_preset: Technical quality settings
            additional_details: Optional additional context
        
        Returns:
            Dict with 'positive_prompt' and 'negative_prompt'
        """
        quality_preset = quality_preset or {"technical_details": "8K, sharp focus, professional", "emphasis_weight": 1.2}
        weight = quality_preset.get("emphasis_weight", 1.2)
        
        # Determine image type based on art style
        style_lower = art_style.lower()
        if "photo" in style_lower or "realistic" in style_lower:
            image_type = "portrait photograph"
        elif "3d" in style_lower or "render" in style_lower:
            image_type = "3D character render"
        else:
            image_type = "character portrait"
        
        # Build subject with emphasis
        subject = cls.apply_emphasis(f"{character_name}, {character_type}", weight)
        
        # Extract and emphasize key visual features
        appearance_emphasized = cls._emphasize_key_features(appearance, weight * 0.9)
        
        # Pose and action
        action = pose if pose else "standing pose, confident stance"
        
        # Setting (for character sheets, usually neutral or thematic background)
        setting = "neutral background" if not additional_details else additional_details.get("setting", "neutral background")
        setting_weighted = f"[{setting}:0.8]"  # Lower weight for background
        
        # Style
        style_desc = cls.ART_STYLES.get(style_lower.split()[0], art_style)
        style_emphasized = cls.apply_emphasis(style_desc, weight)
        
        # Lighting
        lighting = "soft natural lighting, rim light on edges"
        
        # Color palette
        color_desc = f", {color_palette}" if color_palette else ""
        
        # Technical details
        technical = quality_preset.get("technical_details", "8K, sharp focus, professional")
        
        # Construct positive prompt
        positive_parts = [
            image_type,
            "of",
            subject,
            appearance_emphasized,
            action,
            setting_weighted,
            style_emphasized,
            lighting,
            technical
        ]
        
        positive_prompt = ", ".join(filter(None, positive_parts))
        if color_desc:
            positive_prompt += color_desc
        
        # Build negative prompt
        negative_prompt = cls._build_negative_prompt(
            character_type,
            include_anatomy=True,
            additional_negatives=["multiple people", "crowd", "group"]
        )
        
        return {
            "positive_prompt": positive_prompt,
            "negative_prompt": negative_prompt
        }
    
    @classmethod
    def build_environment_prompt(
        cls,
        location_name: str,
        location_type: str,
        description: str,
        atmosphere: str,
        art_style: str,
        key_features: List[str] = None,
        time_of_day: str = "",
        weather: str = "",
        quality_preset: Dict[str, Any] = None
    ) -> Dict[str, str]:
        """
        Build optimized environment/location prompt.
        
        Args:
            location_name: Name of the location
            location_type: Type (City, Dungeon, Forest, Castle, etc.)
            description: Detailed visual description
            atmosphere: Mood and atmosphere
            art_style: Art style keyword
            key_features: Notable architectural/design elements
            time_of_day: Time (morning, sunset, night, etc.)
            weather: Weather conditions
            quality_preset: Technical quality settings
        
        Returns:
            Dict with 'positive_prompt' and 'negative_prompt'
        """
        quality_preset = quality_preset or {"technical_details": "8K, sharp focus, professional", "emphasis_weight": 1.2}
        weight = quality_preset.get("emphasis_weight", 1.2)
        
        # Image type
        style_lower = art_style.lower()
        if "photo" in style_lower:
            image_type = "landscape photograph"
        elif "3d" in style_lower:
            image_type = "3D environment render"
        else:
            image_type = "environment concept art"
        
        # Subject - location with emphasis
        subject = cls.apply_emphasis(f"{location_type}", weight)
        
        # Description with key features emphasized
        desc_parts = [description[:200]]  # Limit description length
        if key_features:
            features = ", ".join(key_features[:3])  # Top 3 features
            features_emphasized = cls.apply_emphasis(features, weight * 1.1)
            desc_parts.append(features_emphasized)
        
        description_text = ", ".join(desc_parts)
        
        # Setting context (time, weather)
        setting_parts = []
        if time_of_day:
            setting_parts.append(time_of_day)
        if weather:
            setting_parts.append(weather)
        setting = ", ".join(setting_parts) if setting_parts else "clear day"
        
        # Atmosphere/mood
        atmosphere_emphasized = cls.apply_emphasis(atmosphere, weight * 0.9)
        
        # Style
        style_desc = cls.ART_STYLES.get(style_lower.split()[0], art_style)
        style_emphasized = cls.apply_emphasis(style_desc, weight)
        
        # Lighting based on atmosphere and time
        if "dark" in atmosphere.lower() or "night" in time_of_day.lower():
            lighting = cls.LIGHTING_PRESETS["dramatic"]
        elif "magical" in atmosphere.lower() or "mystical" in atmosphere.lower():
            lighting = cls.LIGHTING_PRESETS["magical"]
        else:
            lighting = cls.LIGHTING_PRESETS["natural"]
        
        # Technical
        technical = quality_preset.get("technical_details", "8K, sharp focus, professional")
        
        # Construct positive prompt
        positive_parts = [
            image_type,
            "of",
            subject,
            description_text,
            setting,
            atmosphere_emphasized,
            style_emphasized,
            lighting,
            technical,
            "no people"
        ]
        
        positive_prompt = ", ".join(filter(None, positive_parts))
        
        # Negative prompt
        negative_prompt = cls._build_negative_prompt(
            "environment",
            include_anatomy=False,
            additional_negatives=["people", "characters", "humans", "crowds", "cluttered"]
        )
        
        return {
            "positive_prompt": positive_prompt,
            "negative_prompt": negative_prompt
        }
    
    @classmethod
    def build_item_prompt(
        cls,
        item_name: str,
        item_type: str,
        description: str,
        materials: str,
        art_style: str,
        special_properties: List[str] = None,
        scale_reference: str = "",
        quality_preset: Dict[str, Any] = None
    ) -> Dict[str, str]:
        """
        Build optimized item/equipment prompt.
        
        Args:
            item_name: Name of the item
            item_type: Type (Weapon, Armor, Artifact, etc.)
            description: Detailed visual description
            materials: Material composition
            art_style: Art style keyword
            special_properties: Magical/special visual effects
            scale_reference: Size reference
            quality_preset: Technical quality settings
        
        Returns:
            Dict with 'positive_prompt' and 'negative_prompt'
        """
        quality_preset = quality_preset or {"technical_details": "8K, sharp focus, professional", "emphasis_weight": 1.3}
        weight = quality_preset.get("emphasis_weight", 1.3)
        
        # Image type - product shot for items
        image_type = "product shot" if "realistic" in art_style.lower() else "item concept art"
        
        # Subject with emphasis
        subject = cls.apply_emphasis(f"{item_name}, {item_type}", weight)
        
        # Description with materials
        desc_parts = [description, f"made of {materials}"]
        
        # Special properties emphasized
        if special_properties:
            properties = ", ".join(special_properties)
            properties_emphasized = cls.apply_emphasis(properties, weight * 1.2)
            desc_parts.append(properties_emphasized)
        
        description_text = ", ".join(filter(None, desc_parts))
        
        # Scale reference
        scale = scale_reference if scale_reference else ""
        
        # Setting
        setting = "neutral background, studio setup"
        
        # Style
        style_lower = art_style.lower()
        style_desc = cls.ART_STYLES.get(style_lower.split()[0], art_style)
        style_emphasized = cls.apply_emphasis(style_desc, weight)
        
        # Lighting - studio lighting for items
        lighting = cls.LIGHTING_PRESETS["studio"]
        
        # Technical - extra detail for items
        technical = quality_preset.get("technical_details", "8K, ultra detailed, sharp focus")
        technical += ", shallow depth of field, macro lens"
        
        # Construct positive prompt
        positive_parts = [
            image_type,
            "of",
            subject,
            description_text,
            scale,
            setting,
            style_emphasized,
            lighting,
            technical
        ]
        
        positive_prompt = ", ".join(filter(None, positive_parts))
        
        # Negative prompt
        negative_prompt = cls._build_negative_prompt(
            "item",
            include_anatomy=False,
            additional_negatives=["hand holding", "person", "wrist", "fingers", "clutter"]
        )
        
        return {
            "positive_prompt": positive_prompt,
            "negative_prompt": negative_prompt
        }
    
    @classmethod
    def build_storyboard_prompt(
        cls,
        scene_name: str,
        visual_composition: str,
        key_elements: List[str],
        narrative_context: str,
        mood_tone: str,
        art_style: str,
        color_palette: str = "",
        quality_preset: Dict[str, Any] = None
    ) -> Dict[str, str]:
        """
        Build optimized storyboard/key art prompt.
        
        Args:
            scene_name: Name of the scene
            visual_composition: Framing and composition
            key_elements: Characters, objects, environmental elements
            narrative_context: What's happening in the scene
            mood_tone: Emotional tone
            art_style: Art style keyword
            color_palette: Color scheme
            quality_preset: Technical quality settings
        
        Returns:
            Dict with 'positive_prompt' and 'negative_prompt'
        """
        quality_preset = quality_preset or {"technical_details": "8K, sharp focus, cinematic", "emphasis_weight": 1.3}
        weight = quality_preset.get("emphasis_weight", 1.3)
        
        # Image type - cinematic for storyboards
        image_type = "cinematic scene"
        
        # Subject - scene name with emphasis
        subject = cls.apply_emphasis(scene_name, weight)
        
        # Key elements with emphasis
        elements_text = ", ".join(key_elements[:5])  # Top 5 elements
        elements_emphasized = cls.apply_emphasis(elements_text, weight * 1.1)
        
        # Narrative action
        action = narrative_context[:150]  # Limit length
        
        # Visual composition
        composition_emphasized = cls.apply_emphasis(visual_composition, weight * 0.9)
        
        # Mood/atmosphere
        mood_emphasized = cls.apply_emphasis(mood_tone, weight * 1.2)
        
        # Style
        style_lower = art_style.lower()
        style_desc = cls.ART_STYLES.get(style_lower.split()[0], art_style)
        style_emphasized = cls.apply_emphasis(style_desc + ", cinematic", weight)
        
        # Lighting - dramatic for storyboards
        lighting = cls.LIGHTING_PRESETS["dramatic"]
        
        # Color palette
        color_desc = f", {color_palette}" if color_palette else ""
        
        # Technical - cinematic quality
        technical = quality_preset.get("technical_details", "8K, cinematic, professional")
        technical += ", wide shot, establishing shot"
        
        # Construct positive prompt
        positive_parts = [
            image_type,
            subject,
            elements_emphasized,
            action,
            composition_emphasized,
            mood_emphasized,
            style_emphasized,
            lighting,
            technical
        ]
        
        positive_prompt = ", ".join(filter(None, positive_parts))
        if color_desc:
            positive_prompt += color_desc
        
        # Negative prompt
        negative_prompt = cls._build_negative_prompt(
            "scene",
            include_anatomy=True,
            additional_negatives=["static", "boring", "flat lighting", "poorly composed"]
        )
        
        return {
            "positive_prompt": positive_prompt,
            "negative_prompt": negative_prompt
        }
    
    @classmethod
    def _emphasize_key_features(cls, text: str, weight: float) -> str:
        """
        Extract and emphasize key visual features from description.
        
        Args:
            text: Description text
            weight: Emphasis weight
        
        Returns:
            Text with key features emphasized
        """
        # Simple keyword emphasis - in production, could use NLP
        keywords = [
            "hair", "eyes", "armor", "weapon", "cloak", "robe",
            "crown", "staff", "sword", "shield", "helmet",
            "tattoo", "scar", "jewelry", "wings", "horns"
        ]
        
        result = text
        for keyword in keywords:
            pattern = rf"\b({keyword}[a-z]*)\b"
            result = re.sub(
                pattern,
                lambda m: cls.apply_emphasis(m.group(1), weight),
                result,
                flags=re.IGNORECASE,
                count=1  # Only emphasize first occurrence
            )
        
        return result
    
    @classmethod
    def _build_negative_prompt(
        cls,
        content_type: str,
        include_anatomy: bool = True,
        additional_negatives: List[str] = None
    ) -> str:
        """
        Build comprehensive negative prompt.
        
        Args:
            content_type: Type of content (character, environment, item, scene)
            include_anatomy: Whether to include anatomy-related negatives
            additional_negatives: Additional negative terms
        
        Returns:
            Comma-separated negative prompt
        """
        negatives = []
        
        # Always include quality issues
        negatives.extend(cls.NEGATIVE_QUALITY)
        
        # Include anatomy issues if requested
        if include_anatomy:
            negatives.extend(cls.NEGATIVE_ANATOMY)
        
        # Always include unwanted elements
        negatives.extend(cls.NEGATIVE_UNWANTED)
        
        # Add additional negatives
        if additional_negatives:
            negatives.extend(additional_negatives)
        
        return ", ".join(negatives)
    
    @staticmethod
    def truncate_prompt(prompt: str, max_length: int = 500) -> str:
        """
        Truncate prompt to maximum length while preserving emphasis syntax.
        
        Args:
            prompt: Prompt text
            max_length: Maximum character length
        
        Returns:
            Truncated prompt
        """
        if len(prompt) <= max_length:
            return prompt
        
        # Truncate at last comma before max_length
        truncated = prompt[:max_length]
        last_comma = truncated.rfind(",")
        
        if last_comma > 0:
            return truncated[:last_comma].strip()
        
        return truncated.strip()

