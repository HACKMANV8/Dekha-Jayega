#!/usr/bin/env python3
"""
Run Orchestrator Agent

This script provides a user-friendly interface to run the orchestrator agent,
which analyzes existing user_view files and selectively updates components
based on LLM feedback.

Usage:
    python run_orchestrator.py <user_view_file.json> [options]

Options:
    --confirm       Prompt for confirmation before applying updates (default: auto-apply)
    --interactive   Use interactive mode with component-by-component confirmation
    --feedback      Provide custom feedback (will prompt for input)
    --full-analysis Analyze all components (default: only update what's mentioned in feedback)
    --model         Specify model to use (e.g., gpt-5, gemini-2.5-pro)
    --help          Show this help message

Examples:
    # Targeted update (only updates what you mention - DEFAULT)
    python run_orchestrator.py ArcueAgent/exports/Story_USER_VIEW_20231022.json

    # Full analysis mode (analyzes and updates all components)
    python run_orchestrator.py ArcueAgent/exports/Story_USER_VIEW_20231022.json --full-analysis

    # With confirmation prompt
    python run_orchestrator.py ArcueAgent/exports/Story_USER_VIEW_20231022.json --confirm

    # Interactive mode with component-by-component confirmation
    python run_orchestrator.py ArcueAgent/exports/Story_USER_VIEW_20231022.json --interactive

    # Use specific model
    python run_orchestrator.py ArcueAgent/exports/Story_USER_VIEW_20231022.json --model gemini-2.5-pro
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path (parent of OrchestratorAgent)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from OrchestratorAgent.orchestrator import OrchestratorAgent
from SagaAgent.config import AgentConfig


def print_banner():
    """Print a nice banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              🎬 ARCUE AGENT ORCHESTRATOR 🎬                      ║
║                                                                   ║
║          AI-Powered Story Revision & Component Updates           ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_help():
    """Print help message"""
    print(__doc__)


def main():
    """Main entry point"""
    
    # Check for help flag
    if '--help' in sys.argv or '-h' in sys.argv or len(sys.argv) < 2:
        print_help()
        sys.exit(0 if '--help' in sys.argv or '-h' in sys.argv else 1)
    
    print_banner()
    
    # Parse arguments
    user_view_file = sys.argv[1]
    confirm_before_apply = '--confirm' in sys.argv
    auto_apply = not confirm_before_apply  # Default is True (auto-apply), unless --confirm is specified
    interactive = '--interactive' in sys.argv
    use_feedback = '--feedback' in sys.argv
    full_analysis = '--full-analysis' in sys.argv
    targeted_update = not full_analysis  # Default is True (targeted), unless --full-analysis is specified
    
    # Check if file exists
    if not os.path.exists(user_view_file):
        print(f"[ERROR] File not found: {user_view_file}")
        print(f"\nPlease provide a valid user_view JSON file.")
        sys.exit(1)
    
    # Check for model override
    model = None
    if '--model' in sys.argv:
        try:
            model_idx = sys.argv.index('--model')
            if model_idx + 1 < len(sys.argv):
                model = sys.argv[model_idx + 1]
                os.environ['MODEL'] = model
                print(f"🤖 Using model: {model}\n")
        except (ValueError, IndexError):
            print("[WARNING] --model flag provided but no model specified. Using default.")
    
    # Create agent config
    agent_config = AgentConfig.from_env()
    
    # Print configuration
    print(f"📋 Configuration:")
    print(f"   Model: {agent_config.model}")
    if agent_config.model_temperature:
        print(f"   Temperature: {agent_config.model_temperature}")
    
    if interactive:
        mode_display = "Interactive (component-by-component)"
    elif auto_apply:
        mode_display = "Auto-apply (default - no confirmation)"
    else:
        mode_display = "Confirm (prompt before applying)"
    print(f"   Mode: {mode_display}")
    
    update_strategy = "Full analysis (all components)" if full_analysis else "Targeted (only what you mention)"
    print(f"   Update Strategy: {update_strategy}")
    print()
    
    # Create orchestrator
    orchestrator = OrchestratorAgent(agent_config)
    
    try:
        # Get user feedback if requested
        user_feedback = ""
        if use_feedback and not interactive:
            print("📝 Please provide your feedback for the story:")
            print("   (Press Enter twice when done)")
            lines = []
            while True:
                line = input()
                if line == "" and len(lines) > 0:
                    break
                lines.append(line)
            user_feedback = "\n".join(lines)
            print()
        
        # Run appropriate workflow
        if interactive:
            new_json, new_markdown = orchestrator.interactive_revision(user_view_file)
        else:
            new_json, new_markdown = orchestrator.orchestrate_revision(
                user_view_file,
                user_feedback=user_feedback,
                auto_apply=auto_apply,
                targeted_update=targeted_update
            )
        
        # Success message
        if new_json and new_markdown:
            print("\n[SUCCESS] Story has been revised and exported.")
            print(f"\nNew files created:")
            print(f"   JSON: {new_json}")
            print(f"   Markdown: {new_markdown}")
            print(f"\nTip: You can run the orchestrator again on the new file for further refinement.")
        else:
            print("\n[WARNING] No files were created (revision may have been cancelled).")
        
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Interrupted by user. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Error during orchestration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

