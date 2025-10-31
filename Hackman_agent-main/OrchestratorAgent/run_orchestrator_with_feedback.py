#!/usr/bin/env python3
"""
Helper script to run orchestrator with specific feedback
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

def main():
    if len(sys.argv) < 3:
        print("Usage: python run_orchestrator_with_feedback.py <user_view_file> <feedback> [--use-react]")
        print("\nOptions:")
        print("  --use-react    Use ReAct agent pattern for intelligent reasoning (default: True)")
        print("  --no-react     Use direct LLM call instead of ReAct agent")
        sys.exit(1)
    
    user_view_file = sys.argv[1]
    feedback = sys.argv[2]
    use_react = '--no-react' not in sys.argv  # Default is True
    
    print("\n" + "="*70)
    print("ORCHESTRATOR WITH CUSTOM FEEDBACK")
    print("="*70)
    print(f"File: {user_view_file}")
    print(f"Feedback: {feedback}")
    print(f"Mode: {'ReAct Agent' if use_react else 'Direct LLM'}")
    print("="*70 + "\n")
    
    # Create orchestrator with ReAct agent
    agent_config = AgentConfig.from_env()
    orchestrator = OrchestratorAgent(agent_config, use_react=use_react)
    
    # Run orchestration with feedback (auto_apply=True, targeted_update=True by default)
    new_json, new_markdown = orchestrator.orchestrate_revision(
        user_view_filepath=user_view_file,
        user_feedback=feedback,
        auto_apply=True,  # Auto-apply by default
        targeted_update=True  # Only update what's mentioned in feedback
    )
    
    if new_json and new_markdown:
        print("\n[SUCCESS] New files created:")
        print(f"   JSON: {new_json}")
        print(f"   Markdown: {new_markdown}")
    else:
        print("\n[WARNING] No files were created.")

if __name__ == "__main__":
    main()

