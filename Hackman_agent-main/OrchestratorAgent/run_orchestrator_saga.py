"""
Run the Orchestrator Agent for SagaAgent with command-line interface.

This script provides a user-friendly CLI for the orchestrator agent,
allowing you to revise saga narrative components with LLM-powered feedback.

Usage:
    python run_orchestrator_saga.py <saga_file_or_directory> [options]

Examples:
    # Auto-apply all updates
    python run_orchestrator_saga.py SagaAgent/exports/ --auto

    # With specific feedback
    python run_orchestrator_saga.py saga_characters.json --feedback "Add Marcus as a rebel leader"

    # Interactive mode with confirmation
    python run_orchestrator_saga.py SagaAgent/exports/ --feedback "Make factions more complex"

    # Use specific model
    python run_orchestrator_saga.py saga_factions.json --model gemini-2.0-flash-exp --auto
"""

import sys
import os
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from OrchestratorAgent.orchestrator_saga import OrchestratorAgent
from SagaAgent.config import AgentConfig


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description="Orchestrator Agent for SagaAgent - AI-powered game narrative revision",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-apply updates to all components in a directory
  python run_orchestrator_saga.py SagaAgent/exports/ --auto

  # Update a specific component with feedback
  python run_orchestrator_saga.py saga_characters.json --feedback "Add a character named Elena"

  # Use a specific model
  python run_orchestrator_saga.py saga_factions.json --model gemini-2.0-flash-exp --auto

  # Analyze without auto-applying (interactive mode)
  python run_orchestrator_saga.py SagaAgent/exports/ --feedback "Improve character depth"
        """
    )
    
    parser.add_argument(
        "saga_path",
        help="Path to saga file (.json) or directory containing saga files"
    )
    
    parser.add_argument(
        "--feedback",
        "-f",
        type=str,
        default="",
        help="User feedback for targeted component updates"
    )
    
    parser.add_argument(
        "--auto",
        "-a",
        action="store_true",
        help="Automatically apply all updates without confirmation"
    )
    
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default=None,
        help="LLM model to use (e.g., gpt-4o, gemini-2.0-flash-exp)"
    )
    
    parser.add_argument(
        "--temperature",
        "-t",
        type=float,
        default=None,
        help="Model temperature (0.0-1.0)"
    )
    
    parser.add_argument(
        "--full-analysis",
        action="store_true",
        help="Perform full analysis of all components (default: targeted update)"
    )
    
    args = parser.parse_args()
    
    # Validate saga path
    if not os.path.exists(args.saga_path):
        print(f"Error: Path not found: {args.saga_path}")
        sys.exit(1)
    
    # Create config
    config = AgentConfig.from_env()
    
    # Override with command-line arguments
    if args.model:
        config.model = args.model
    if args.temperature is not None:
        config.model_temperature = args.temperature
    
    print(f"\n{'='*70}")
    print(f"ORCHESTRATOR AGENT FOR SAGAAGENT")
    print(f"{'='*70}")
    print(f"Model: {config.model}")
    print(f"Temperature: {config.model_temperature}")
    print(f"Auto-apply: {args.auto}")
    print(f"Mode: {'Full Analysis' if args.full_analysis else 'Targeted Update'}")
    print(f"{'='*70}\n")
    
    # Create orchestrator
    orchestrator = OrchestratorAgent(agent_config=config)
    
    # Run orchestration
    try:
        json_files, markdown_files = orchestrator.orchestrate_revision(
            saga_filepath=args.saga_path,
            user_feedback=args.feedback,
            auto_apply=args.auto,
            targeted_update=not args.full_analysis
        )
        
        if json_files or markdown_files:
            print(f"\n✅ Revision complete!")
            print(f"Generated {len(json_files)} JSON files and {len(markdown_files)} Markdown files")
        else:
            print(f"\n⚠️ No files were generated. Review the feedback and try again.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


