"""
Export Service for RenderPrepAgent.

Handles exporting image prompts, metadata, and generated images to JSON and Markdown.
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Any
from RenderPrepAgent.config import RenderConfig


class RenderExportService:
    """Service for exporting render prep data"""
    
    @staticmethod
    def _ensure_export_dir() -> str:
        """Ensure export directory exists and return path"""
        os.makedirs(RenderConfig.EXPORT_DIR, exist_ok=True)
        return RenderConfig.EXPORT_DIR
    
    @staticmethod
    def _get_filename_base(state: dict) -> tuple:
        """Get timestamp and sanitized title for filenames"""
        import re
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        saga_data = state.get("saga_data", {})
        concept = saga_data.get("concept", {})
        title = concept.get("title", "Untitled_Saga") if isinstance(concept, dict) else "Untitled_Saga"
        
        # Sanitize filename
        title = re.sub(r'[<>:"/\\|?*]', '_', title)
        title = title.replace(" ", "_")
        title = re.sub(r'_+', '_', title)
        title = title.strip('_')
        
        return timestamp, title
    
    @staticmethod
    def export_prompts_json(
        prompts: List[Dict[str, Any]],
        prompt_type: str,
        state: dict
    ) -> str:
        """
        Export prompt data to JSON.
        
        Args:
            prompts: List of prompt dictionaries
            prompt_type: Type (characters, environments, items, storyboards)
            state: Current state
        
        Returns:
            Path to exported JSON file
        """
        export_dir = RenderExportService._ensure_export_dir()
        timestamp, title = RenderExportService._get_filename_base(state)
        
        filename = f"{export_dir}{title}_{prompt_type}_prompts_{timestamp}.json"
        
        export_data = {
            "type": prompt_type,
            "title": title,
            "timestamp": timestamp,
            "count": len(prompts),
            "prompts": prompts
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Exported {prompt_type} prompts: {filename}")
        return filename
    
    @staticmethod
    def export_prompts_markdown(
        prompts: List[Dict[str, Any]],
        prompt_type: str,
        state: dict
    ) -> str:
        """
        Export prompt data to Markdown.
        
        Args:
            prompts: List of prompt dictionaries
            prompt_type: Type (characters, environments, items, storyboards)
            state: Current state
        
        Returns:
            Path to exported Markdown file
        """
        export_dir = RenderExportService._ensure_export_dir()
        timestamp, title = RenderExportService._get_filename_base(state)
        
        filename = f"{export_dir}{title}_{prompt_type}_prompts_{timestamp}.md"
        
        content = f"# {prompt_type.title()} Image Prompts - {title}\n\n"
        content += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n"
        content += f"**Count:** {len(prompts)} prompts\n\n"
        content += "---\n\n"
        
        for i, prompt in enumerate(prompts, 1):
            content += f"## {i}. {prompt.get('name', 'Unnamed')}\n\n"
            
            # Type/ID
            if prompt.get('id'):
                content += f"**ID:** `{prompt['id']}`  \n"
            if prompt.get('type'):
                content += f"**Type:** {prompt['type']}  \n\n"
            
            # Positive Prompt
            content += "### Positive Prompt\n\n"
            content += f"```\n{prompt.get('positive_prompt', 'N/A')}\n```\n\n"
            
            # Negative Prompt
            content += "### Negative Prompt\n\n"
            content += f"```\n{prompt.get('negative_prompt', 'N/A')}\n```\n\n"
            
            # Original Description
            if prompt.get('original_description'):
                content += "### Original Description\n\n"
                content += f"{prompt['original_description']}\n\n"
            
            # Metadata
            if prompt.get('metadata'):
                content += "### Metadata\n\n"
                for key, value in prompt['metadata'].items():
                    content += f"- **{key}:** {value}\n"
                content += "\n"
            
            # Generated Image (if available)
            if prompt.get('generated_image_url'):
                content += "### Generated Image\n\n"
                content += f"![{prompt.get('name')}]({prompt['generated_image_url']})\n\n"
            
            content += "---\n\n"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✓ Exported {prompt_type} prompts: {filename}")
        return filename
    
    @staticmethod
    def export_all(state: dict) -> dict:
        """
        Export all render prep data.
        
        Args:
            state: Current RenderPrepState
        
        Returns:
            Dict with export results
        """
        print("\n--- EXPORTING RENDER PREP DATA ---")
        
        export_dir = RenderExportService._ensure_export_dir()
        timestamp, title = RenderExportService._get_filename_base(state)
        
        json_files = []
        md_files = []
        
        # Export character prompts
        if state.get("character_prompts"):
            json_files.append(
                RenderExportService.export_prompts_json(
                    state["character_prompts"], "characters", state
                )
            )
            md_files.append(
                RenderExportService.export_prompts_markdown(
                    state["character_prompts"], "characters", state
                )
            )
        
        # Export environment prompts
        if state.get("environment_prompts"):
            json_files.append(
                RenderExportService.export_prompts_json(
                    state["environment_prompts"], "environments", state
                )
            )
            md_files.append(
                RenderExportService.export_prompts_markdown(
                    state["environment_prompts"], "environments", state
                )
            )
        
        # Export item prompts
        if state.get("item_prompts"):
            json_files.append(
                RenderExportService.export_prompts_json(
                    state["item_prompts"], "items", state
                )
            )
            md_files.append(
                RenderExportService.export_prompts_markdown(
                    state["item_prompts"], "items", state
                )
            )
        
        # Export storyboard prompts
        if state.get("storyboard_prompts"):
            json_files.append(
                RenderExportService.export_prompts_json(
                    state["storyboard_prompts"], "storyboards", state
                )
            )
            md_files.append(
                RenderExportService.export_prompts_markdown(
                    state["storyboard_prompts"], "storyboards", state
                )
            )
        
        # Export master summary
        summary_file = RenderExportService._export_summary(state, timestamp, title)
        json_files.append(summary_file)
        
        print(f"\n✓ All exports complete: {export_dir}")
        print(f"  - {len(json_files)} JSON files")
        print(f"  - {len(md_files)} Markdown files")
        
        return {
            "export_path": export_dir,
            "export_timestamp": timestamp,
            "json_files": json_files,
            "markdown_files": md_files
        }
    
    @staticmethod
    def _export_summary(state: dict, timestamp: str, title: str) -> str:
        """Export master summary JSON."""
        export_dir = RenderExportService._ensure_export_dir()
        filename = f"{export_dir}{title}_render_summary_{timestamp}.json"
        
        summary = {
            "title": title,
            "timestamp": timestamp,
            "quality_preset": state.get("quality_preset", "standard"),
            "statistics": {
                "character_prompts": len(state.get("character_prompts", [])),
                "environment_prompts": len(state.get("environment_prompts", [])),
                "item_prompts": len(state.get("item_prompts", [])),
                "storyboard_prompts": len(state.get("storyboard_prompts", [])),
                "total_prompts": (
                    len(state.get("character_prompts", [])) +
                    len(state.get("environment_prompts", [])) +
                    len(state.get("item_prompts", [])) +
                    len(state.get("storyboard_prompts", []))
                )
            },
            "generated_images": state.get("generated_images", []) if state.get("generate_images") else [],
            "errors": state.get("errors", [])
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        return filename

