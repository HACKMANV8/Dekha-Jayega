"""Image generation node for actually generating images via Nano Banana API."""
from typing import Dict, Any, List
from RenderPrepAgent.services.nano_banana_service import NanoBananaSyncService
from RenderPrepAgent.config import RenderConfig


def generate_images_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate actual images via Nano Banana API (optional).
    
    Only runs if state["generate_images"] is True.
    
    Args:
        state: RenderPrepState with all prompts
    
    Returns:
        Dict with generated_images list
    """
    # Check if image generation is enabled
    if not state.get("generate_images", False):
        print("\n--- SKIPPING IMAGE GENERATION (generate_images=False) ---")
        return {"generated_images": []}
    
    print("\n--- NODE: GENERATING IMAGES VIA NANO BANANA ---")
    
    # Initialize Nano Banana service
    service = NanoBananaSyncService()
    
    # Collect all prompts
    all_prompts = []
    
    # Character prompts
    for char_prompt in state.get("character_prompts", []):
        all_prompts.append({
            "positive_prompt": char_prompt["positive_prompt"],
            "negative_prompt": char_prompt["negative_prompt"],
            "metadata": {
                "type": "character",
                "name": char_prompt["name"],
                "id": char_prompt["id"]
            }
        })
    
    # Environment prompts
    for env_prompt in state.get("environment_prompts", []):
        all_prompts.append({
            "positive_prompt": env_prompt["positive_prompt"],
            "negative_prompt": env_prompt["negative_prompt"],
            "metadata": {
                "type": "environment",
                "name": env_prompt["name"],
                "id": env_prompt["id"]
            }
        })
    
    # Item prompts
    for item_prompt in state.get("item_prompts", []):
        all_prompts.append({
            "positive_prompt": item_prompt["positive_prompt"],
            "negative_prompt": item_prompt["negative_prompt"],
            "metadata": {
                "type": "item",
                "name": item_prompt["name"],
                "id": item_prompt["id"]
            }
        })
    
    # Storyboard prompts
    for story_prompt in state.get("storyboard_prompts", []):
        all_prompts.append({
            "positive_prompt": story_prompt["positive_prompt"],
            "negative_prompt": story_prompt["negative_prompt"],
            "metadata": {
                "type": "storyboard",
                "name": story_prompt["name"],
                "id": story_prompt["id"]
            }
        })
    
    if not all_prompts:
        print("⚠ No prompts to generate images from")
        return {"generated_images": []}
    
    print(f"  Generating {len(all_prompts)} images...")
    
    # Get quality settings
    quality_preset = state.get("quality_preset", "standard")
    image_size = RenderConfig.DEFAULT_IMAGE_SIZE
    
    # Generate images in batch
    try:
        results = service.generate_batch(
            prompts=all_prompts,
            image_size=image_size,
            quality=quality_preset
        )
        
        generated_images = []
        errors = []
        
        for result in results:
            if result["success"]:
                generated_images.extend(result["images"])
                print(f"  ✓ Generated: {result['metadata'].get('name', 'Unknown')}")
            else:
                error_msg = f"Failed to generate {result['metadata'].get('name', 'Unknown')}: {result.get('error', 'Unknown error')}"
                errors.append(error_msg)
                print(f"  ✗ {error_msg}")
        
        # Close service
        service.close()
        
        print(f"\n✓ Image generation complete: {len(generated_images)} images generated")
        if errors:
            print(f"⚠ {len(errors)} errors encountered")
        
        return {
            "generated_images": generated_images,
            "errors": errors if errors else []
        }
    
    except Exception as e:
        error_msg = f"Image generation failed: {str(e)}"
        print(f"✗ {error_msg}")
        service.close()
        
        return {
            "generated_images": [],
            "errors": [error_msg]
        }

