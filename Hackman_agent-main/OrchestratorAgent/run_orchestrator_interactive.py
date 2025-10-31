#!/usr/bin/env python3
"""
Interactive orchestrator - automatically uses latest user_view file.
User just provides what they want to change.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from OrchestratorAgent.orchestrator import OrchestratorAgent
from OrchestratorAgent.utils.file_utils import find_latest_user_view, list_recent_user_views, format_file_info
from SagaAgent.config import AgentConfig


def print_banner():
    """Print welcome banner."""
    print("\n" + "="*70)
    print("   🎬 ORCHESTRATOR AGENT - INTERACTIVE MODE")
    print("="*70)
    print()


def select_user_view(auto_latest: bool = True) -> str:
    """
    Select a user_view file to work with.
    
    Args:
        auto_latest: If True, automatically use latest. If False, show options.
        
    Returns:
        Path to selected user_view file
    """
    if auto_latest:
        # Automatically use latest
        latest = find_latest_user_view()
        if not latest:
            print("[ERROR] No user_view files found in ArcueAgent/exports/")
            print("   Please generate a story first using ArcueAgent")
            sys.exit(1)
        
        info = format_file_info(latest)
        print("[INFO] Using Latest User View:")
        print(f"   File: {info['filename']}")
        print(f"   Title: {info.get('title', 'Unknown')}")
        print(f"   Genre: {info.get('genre', 'Unknown')}")
        print(f"   Modified: {info['modified']}")
        print(f"   Characters: {info.get('characters', 0)}")
        print(f"   Scenes: {info.get('scenes', 0)}")
        print()
        
        return latest
    else:
        # Show options and let user choose
        recent_files = list_recent_user_views(limit=5)
        
        if not recent_files:
            print("[ERROR] No user_view files found in ArcueAgent/exports/")
            sys.exit(1)
        
        print("[INFO] Recent User View Files:")
        print()
        
        for i, filepath in enumerate(recent_files, 1):
            info = format_file_info(filepath)
            print(f"{i}. {info['filename']}")
            print(f"   Title: {info.get('title', 'Unknown')} ({info.get('genre', 'Unknown')})")
            print(f"   Modified: {info['modified']}")
            print()
        
        while True:
            try:
                choice = input(f"Select file (1-{len(recent_files)}) or Enter for latest: ").strip()
                if not choice:
                    return recent_files[0]
                
                idx = int(choice) - 1
                if 0 <= idx < len(recent_files):
                    return recent_files[idx]
                else:
                    print(f"Please enter a number between 1 and {len(recent_files)}")
            except ValueError:
                print("Please enter a valid number")


def get_user_feedback() -> str:
    """
    Get feedback from user about what they want to change.
    
    Returns:
        User's feedback text
    """
    print("="*70)
    print("[INPUT] What would you like to change?")
    print("="*70)
    print()
    print("Examples:")
    print("  • 'Change the cafe to a park'")
    print("  • 'Add a character named Sarah, a thoughtful teacher'")
    print("  • 'Make the dialogue more natural'")
    print("  • 'Add a beach location for sunset scenes'")
    print("  • 'Make the cinematography darker and moodier'")
    print()
    
    feedback = input("Your feedback: ").strip()
    
    if not feedback:
        print("[ERROR] No feedback provided")
        sys.exit(1)
    
    return feedback


def confirm_action(user_view_file: str, feedback: str) -> bool:
    """
    Ask user to confirm the action.
    
    Args:
        user_view_file: Path to user_view file
        feedback: User's feedback
        
    Returns:
        True if user confirms, False otherwise
    """
    print()
    print("="*70)
    print("🔍 CONFIRMATION")
    print("="*70)
    print(f"File: {os.path.basename(user_view_file)}")
    print(f"Action: {feedback}")
    print()
    
    confirm = input("Proceed with this update? (yes/no): ").strip().lower()
    return confirm in ['yes', 'y']


def main():
    """Main entry point for interactive orchestrator."""
    print_banner()
    
    # Parse command line arguments
    auto_latest = '--select' not in sys.argv
    use_react = '--no-react' not in sys.argv
    skip_confirm = '--yes' in sys.argv or '-y' in sys.argv
    
    # Check if feedback provided as argument
    feedback_arg = None
    for i, arg in enumerate(sys.argv):
        if arg.startswith('--feedback='):
            feedback_arg = arg.split('=', 1)[1]
        elif arg == '--feedback' and i + 1 < len(sys.argv):
            feedback_arg = sys.argv[i + 1]
    
    # Step 1: Select user_view file
    user_view_file = select_user_view(auto_latest=auto_latest)
    
    # Step 2: Get user feedback
    if feedback_arg:
        feedback = feedback_arg
        print(f"[INPUT] Using feedback: {feedback}\n")
    else:
        feedback = get_user_feedback()
    
    # Step 3: Confirm action
    if not skip_confirm:
        if not confirm_action(user_view_file, feedback):
            print("\n[CANCELLED] Action cancelled by user")
            sys.exit(0)
    
    print()
    print("="*70)
    print("[START] STARTING ORCHESTRATION")
    print("="*70)
    print(f"Mode: {'ReAct Agent' if use_react else 'Direct LLM'}")
    print("="*70)
    print()
    
    # Step 4: Create orchestrator and run
    agent_config = AgentConfig.from_env()
    orchestrator = OrchestratorAgent(agent_config, use_react=use_react)
    
    # Run orchestration with feedback
    new_json, new_markdown = orchestrator.orchestrate_revision(
        user_view_filepath=user_view_file,
        user_feedback=feedback,
        auto_apply=True,
        targeted_update=True
    )
    
    if new_json and new_markdown:
        print("\n" + "="*70)
        print("[SUCCESS]")
        print("="*70)
        print(f"New files created:")
        print(f"  JSON: {new_json}")
        print(f"  Markdown: {new_markdown}")
        print()
        print("Tip: Run again to make more changes to the updated story!")
        print("="*70)
        print()
    else:
        print("\n[WARNING] No files were created.")


def print_help():
    """Print help information."""
    print("""
Usage: python3 OrchestratorAgent/run_orchestrator_interactive.py [OPTIONS]

Interactive orchestrator that automatically uses the latest user_view file.

OPTIONS:
  --select              Show list of recent files to choose from (default: auto-use latest)
  --no-react            Use direct LLM instead of ReAct agent
  --yes, -y             Skip confirmation prompt
  --feedback="text"     Provide feedback as argument instead of interactively
  --help                Show this help message

EXAMPLES:

  # Interactive mode (automatic latest file)
  python3 OrchestratorAgent/run_orchestrator_interactive.py

  # Choose from recent files
  python3 OrchestratorAgent/run_orchestrator_interactive.py --select

  # Provide feedback directly
  python3 OrchestratorAgent/run_orchestrator_interactive.py --feedback="Change the cafe to a park"

  # Skip confirmation
  python3 OrchestratorAgent/run_orchestrator_interactive.py --yes --feedback="Add character Sarah"

  # Use direct LLM (faster)
  python3 OrchestratorAgent/run_orchestrator_interactive.py --no-react

FEEDBACK EXAMPLES:
  • "Change the cafe to a park"
  • "Add a character named Sarah, a thoughtful teacher"
  • "Make the dialogue more natural"
  • "Add a beach location"
  • "Make the cinematography darker"
""")


if __name__ == "__main__":
    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        sys.exit(0)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

