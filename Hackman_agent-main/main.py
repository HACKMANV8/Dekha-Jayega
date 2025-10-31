"""
ScriptEngineX - Main Entry Point

This is the main entry point for running the story generation agent.
For advanced usage and parallel execution, see ArcueAgent/agent.py

[PARALLEL] PARALLEL EXECUTION IS ENABLED BY DEFAULT (40-50% faster!)

The agent runs in parallel mode automatically when AUTO_CONTINUE=true.
This provides 40-50% faster story generation with no additional cost.

To DISABLE parallel mode:
    PARALLEL_EXECUTION=false    # Disable parallel execution
    (or)
    AUTO_CONTINUE=false         # Use sequential mode with manual review

To customize parallel settings:
    PARALLEL_MAX_WORKERS=3      # Number of parallel workers (default: 3)
    PARALLEL_BATCH_SIZE=4       # Scenes per batch (default: 4)

See .env.example for complete configuration options.
"""

from ArcueAgent.agent import main as agent_main


def main():
    """Entry point that delegates to the agent's main function"""
    agent_main()


if __name__ == "__main__":
    main()
