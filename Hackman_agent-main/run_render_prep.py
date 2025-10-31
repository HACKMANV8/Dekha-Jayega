#!/usr/bin/env python3
"""
Wrapper script to run RenderPrepAgent from Node.js backend
Usage: python run_render_prep.py <saga_data_path> [--quality <preset>] [--generate-images]
"""

import sys
import json
import argparse
from pathlib import Path

# Add RenderPrepAgent to path
sys.path.insert(0, str(Path(__file__).parent / "RenderPrepAgent"))

from RenderPrepAgent.agent import run_render_prep
from RenderPrepAgent.config import AgentConfig


def main():
    parser = argparse.ArgumentParser(description="Run RenderPrepAgent on saga data")
    parser.add_argument("saga_data_path", type=str, help="Path to saga data JSON file")
    parser.add_argument(
        "--quality",
        type=str,
        default="standard",
        choices=["draft", "standard", "high", "cinematic"],
        help="Quality preset for prompts",
    )
    parser.add_argument(
        "--generate-images",
        action="store_true",
        help="Generate images using Nano Banana (if configured)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="exports/render_prep",
        help="Output directory for exports",
    )

    args = parser.parse_args()

    try:
        # Load saga data
        with open(args.saga_data_path, "r", encoding="utf-8") as f:
            saga_data = json.load(f)

        print(f"Loaded saga data from {args.saga_data_path}", file=sys.stderr)
        print(f"Quality preset: {args.quality}", file=sys.stderr)
        print(f"Generate images: {args.generate_images}", file=sys.stderr)

        # Create agent config
        agent_config = AgentConfig(
            quality_preset=args.quality,
            generate_images=args.generate_images,
            thread_id=f"render_prep_{Path(args.saga_data_path).stem}",
        )

        # Run RenderPrepAgent
        print("Starting RenderPrepAgent...", file=sys.stderr)
        final_state = run_render_prep(saga_data, agent_config, args.saga_data_path)

        print("RenderPrepAgent completed successfully", file=sys.stderr)
        print(f"Generated {len(final_state.get('character_prompts', []))} character prompts", file=sys.stderr)
        print(f"Generated {len(final_state.get('environment_prompts', []))} environment prompts", file=sys.stderr)
        print(f"Generated {len(final_state.get('item_prompts', []))} item prompts", file=sys.stderr)
        print(f"Generated {len(final_state.get('storyboard_prompts', []))} storyboard prompts", file=sys.stderr)

        # Output success to stdout for Node.js to parse
        output = {
            "success": True,
            "message": "RenderPrepAgent completed successfully",
            "stats": {
                "character_prompts": len(final_state.get("character_prompts", [])),
                "environment_prompts": len(final_state.get("environment_prompts", [])),
                "item_prompts": len(final_state.get("item_prompts", [])),
                "storyboard_prompts": len(final_state.get("storyboard_prompts", [])),
            },
            "export_path": args.output,
        }
        print(json.dumps(output), flush=True)

        return 0

    except FileNotFoundError as e:
        error_msg = f"Saga data file not found: {args.saga_data_path}"
        print(error_msg, file=sys.stderr)
        print(json.dumps({"success": False, "error": error_msg}), flush=True)
        return 1

    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in saga data file: {str(e)}"
        print(error_msg, file=sys.stderr)
        print(json.dumps({"success": False, "error": error_msg}), flush=True)
        return 1

    except Exception as e:
        error_msg = f"RenderPrepAgent error: {str(e)}"
        print(error_msg, file=sys.stderr)
        print(json.dumps({"success": False, "error": error_msg}), flush=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
