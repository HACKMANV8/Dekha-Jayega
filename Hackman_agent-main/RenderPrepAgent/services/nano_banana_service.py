"""
Nano Banana Service for image generation via Google DeepMind's API.

This service handles communication with Nano Banana (Google's AI image generator)
for generating high-fidelity, photorealistic images from text prompts.
"""
import os
import httpx
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class NanoBananaService:
    """
    Integration with Nano Banana (Google DeepMind) image generation API.
    
    Note: As of implementation, Nano Banana may not have a public API yet.
    This service provides a framework for when the API becomes available,
    and includes fallback mechanisms.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        timeout: int = 120
    ):
        """
        Initialize Nano Banana service.
        
        Args:
            api_key: API key for authentication
            endpoint: API endpoint URL
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or os.environ.get("NANO_BANANA_API_KEY", "")
        self.endpoint = endpoint or os.environ.get(
            "NANO_BANANA_ENDPOINT",
            "https://api.google.com/nano-banana/v1"
        )
        self.timeout = timeout
        self.session = httpx.AsyncClient(timeout=timeout)
    
    async def generate_image(
        self,
        positive_prompt: str,
        negative_prompt: str = "",
        image_size: str = "1024x1024",
        num_images: int = 1,
        quality: str = "standard",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate image(s) from text prompt.
        
        Args:
            positive_prompt: Main generation prompt
            negative_prompt: Negative prompt (elements to avoid)
            image_size: Image dimensions (e.g., "1024x1024")
            num_images: Number of images to generate
            quality: Quality preset (draft, standard, premium)
            metadata: Additional metadata to attach
        
        Returns:
            Dict with generated image data:
            {
                "success": bool,
                "images": [{"url": str, "id": str, ...}],
                "metadata": dict,
                "error": str (if failed)
            }
        """
        if not self.api_key:
            return self._mock_generation(
                positive_prompt, negative_prompt, image_size, num_images, metadata
            )
        
        try:
            # Prepare request payload
            payload = {
                "prompt": positive_prompt,
                "negative_prompt": negative_prompt,
                "size": image_size,
                "n": num_images,
                "quality": quality,
                "response_format": "url"
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Make API request
            response = await self.session.post(
                f"{self.endpoint}/generate",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "images": data.get("data", []),
                    "metadata": {
                        "prompt": positive_prompt,
                        "negative_prompt": negative_prompt,
                        "size": image_size,
                        "quality": quality,
                        "timestamp": datetime.now().isoformat(),
                        **(metadata or {})
                    }
                }
            else:
                return {
                    "success": False,
                    "images": [],
                    "error": f"API request failed: {response.status_code} - {response.text}",
                    "metadata": metadata or {}
                }
        
        except Exception as e:
            return {
                "success": False,
                "images": [],
                "error": f"Exception during image generation: {str(e)}",
                "metadata": metadata or {}
            }
    
    async def generate_batch(
        self,
        prompts: List[Dict[str, str]],
        image_size: str = "1024x1024",
        quality: str = "standard"
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple images in batch.
        
        Args:
            prompts: List of prompt dicts with 'positive_prompt', 'negative_prompt', 'metadata'
            image_size: Image dimensions
            quality: Quality preset
        
        Returns:
            List of generation results
        """
        tasks = []
        for prompt_data in prompts:
            task = self.generate_image(
                positive_prompt=prompt_data.get("positive_prompt", ""),
                negative_prompt=prompt_data.get("negative_prompt", ""),
                image_size=image_size,
                quality=quality,
                metadata=prompt_data.get("metadata", {})
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append({
                    "success": False,
                    "images": [],
                    "error": f"Batch generation exception: {str(result)}",
                    "metadata": {}
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    def _mock_generation(
        self,
        positive_prompt: str,
        negative_prompt: str,
        image_size: str,
        num_images: int,
        metadata: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Mock image generation for testing/development when API is unavailable.
        
        Returns mock result structure without actually generating images.
        """
        mock_images = []
        for i in range(num_images):
            mock_images.append({
                "id": f"mock_{datetime.now().timestamp()}_{i}",
                "url": f"https://placeholder.example.com/{image_size}/mock_image_{i}.png",
                "mock": True,
                "note": "This is a mock result. Set NANO_BANANA_API_KEY to generate real images."
            })
        
        return {
            "success": True,
            "images": mock_images,
            "metadata": {
                "prompt": positive_prompt,
                "negative_prompt": negative_prompt,
                "size": image_size,
                "timestamp": datetime.now().isoformat(),
                "mock_mode": True,
                **(metadata or {})
            }
        }
    
    async def close(self):
        """Close the HTTP session."""
        await self.session.aclose()
    
    @staticmethod
    def parse_image_size(size_str: str) -> tuple:
        """
        Parse image size string to tuple.
        
        Args:
            size_str: Size string like "1024x1024"
        
        Returns:
            Tuple (width, height)
        """
        try:
            width, height = size_str.lower().split("x")
            return (int(width), int(height))
        except:
            return (1024, 1024)  # Default
    
    @staticmethod
    def validate_prompt(prompt: str, max_length: int = 500) -> bool:
        """
        Validate prompt meets API requirements.
        
        Args:
            prompt: Prompt text
            max_length: Maximum allowed length
        
        Returns:
            True if valid
        """
        if not prompt or not prompt.strip():
            return False
        
        if len(prompt) > max_length:
            return False
        
        return True


# === Synchronous wrapper for convenience ===
class NanoBananaSyncService:
    """Synchronous wrapper around NanoBananaService."""
    
    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None):
        self.service = NanoBananaService(api_key=api_key, endpoint=endpoint)
    
    def generate_image(
        self,
        positive_prompt: str,
        negative_prompt: str = "",
        image_size: str = "1024x1024",
        num_images: int = 1,
        quality: str = "standard",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Synchronous image generation."""
        return asyncio.run(
            self.service.generate_image(
                positive_prompt, negative_prompt, image_size, num_images, quality, metadata
            )
        )
    
    def generate_batch(
        self,
        prompts: List[Dict[str, str]],
        image_size: str = "1024x1024",
        quality: str = "standard"
    ) -> List[Dict[str, Any]]:
        """Synchronous batch generation."""
        return asyncio.run(self.service.generate_batch(prompts, image_size, quality))
    
    def close(self):
        """Close service."""
        asyncio.run(self.service.close())

