"""
Verification script for SagaAgent implementation.
Tests that all new components work correctly.
"""

def verify_imports():
    """Verify all imports work"""
    print("="*70)
    print("VERIFYING SAGAAGENT IMPLEMENTATION")
    print("="*70)
    
    try:
        # Config imports
        from SagaAgent.config import AgentConfig, ModelConfig, ExportConfig
        print("[OK] Config imports successful")
        print(f"   - Default model: {ModelConfig.get_default_model()}")
        print(f"   - Export dir: {ExportConfig.EXPORT_DIR}")
        print(f"   - OpenAI models: {ModelConfig.get_openai_models()[:3]}...")
        print(f"   - Google models: {ModelConfig.get_google_models()[:3]}...")
        
        # Services imports
        from SagaAgent.services import ExportService
        print("[OK] Services imports successful")
        print(f"   - ExportService available: {ExportService.__name__}")
        
        # Parallel execution imports
        from SagaAgent.utils.parallel_execution import (
            run_parallel_generation,
            ParallelExecutor,
            PerformanceMonitor
        )
        print("[OK] Parallel execution imports successful")
        print(f"   - ParallelExecutor: {ParallelExecutor.__name__}")
        print(f"   - PerformanceMonitor: {PerformanceMonitor.__name__}")
        
        # LLM service imports
        from SagaAgent.utils.llm_service import LLMService
        print("[OK] LLM service imports successful")
        print(f"   - LLMService: {LLMService.__name__}")
        
        # State imports
        from SagaAgent.utils.state import SagaState
        print("[OK] State imports successful")
        print(f"   - SagaState available")
        
        # Agent imports
        from SagaAgent.agent import saga_agent, run_parallel_workflow
        print("[OK] Agent imports successful")
        print(f"   - saga_agent compiled: {saga_agent is not None}")
        print(f"   - run_parallel_workflow available: {run_parallel_workflow.__name__}")
        
        print("\n" + "="*70)
        print("[OK] ALL IMPORTS SUCCESSFUL")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\n[ERROR] IMPORT ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_config():
    """Verify configuration works correctly"""
    print("\n" + "="*70)
    print("VERIFYING CONFIGURATION")
    print("="*70)
    
    try:
        from SagaAgent.config import AgentConfig, ModelConfig
        
        # Test config creation
        config = AgentConfig.from_env()
        print("[OK] AgentConfig created from environment")
        print(f"   - Thread ID: {config.thread_id[:8]}...")
        print(f"   - Auto-continue: {config.auto_continue}")
        print(f"   - Parallel execution: {config.parallel_execution}")
        print(f"   - Max workers: {config.parallel_max_workers}")
        
        # Test state dict conversion
        state_dict = config.to_state_dict()
        print("[OK] Config to state dict conversion works")
        print(f"   - Keys: {list(state_dict.keys())}")
        
        # Test model config
        print("[OK] ModelConfig methods work")
        print(f"   - Default model: {ModelConfig.get_default_model()}")
        print(f"   - OpenAI models count: {len(ModelConfig.get_openai_models())}")
        print(f"   - Google models count: {len(ModelConfig.get_google_models())}")
        
        print("\n" + "="*70)
        print("[OK] CONFIGURATION VERIFICATION COMPLETE")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\n[ERROR] CONFIG ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_export_service():
    """Verify export service functionality"""
    print("\n" + "="*70)
    print("VERIFYING EXPORT SERVICE")
    print("="*70)
    
    try:
        from SagaAgent.services import ExportService
        
        # Test state preparation
        test_state = {
            "concept": {
                "title": "Test Saga",
                "setting": "Fantasy World",
                "core_theme": "Good vs Evil"
            },
            "world_lore": {
                "world_name": "Testlandia",
                "history": "Ancient history",
                "geography": "Mountains and valleys"
            },
            "factions": [
                {"name": "Good Guys", "description": "The heroes"},
                {"name": "Bad Guys", "description": "The villains"}
            ],
            "characters": [
                {"name": "Hero", "role": "protagonist", "background": "Humble origins"}
            ]
        }
        
        # Test formatters (without actually writing files)
        concept_json = ExportService.format_concept_json(test_state)
        print("[OK] format_concept_json works")
        print(f"   - Keys: {list(concept_json.keys())}")
        
        world_json = ExportService.format_world_lore_json(test_state)
        print("[OK] format_world_lore_json works")
        
        factions_json = ExportService.format_factions_json(test_state)
        print("[OK] format_factions_json works")
        print(f"   - Factions count: {len(factions_json['factions'])}")
        
        chars_json = ExportService.format_characters_json(test_state)
        print("[OK] format_characters_json works")
        print(f"   - Characters count: {len(chars_json['characters'])}")
        
        # Test markdown formatters
        concept_md = ExportService.format_concept_markdown(test_state)
        print("[OK] format_concept_markdown works")
        print(f"   - Length: {len(concept_md)} chars")
        
        world_md = ExportService.format_world_lore_markdown(test_state)
        print("[OK] format_world_lore_markdown works")
        
        print("\n" + "="*70)
        print("[OK] EXPORT SERVICE VERIFICATION COMPLETE")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\n[ERROR] EXPORT SERVICE ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all verifications"""
    print("\n")
    print("+" + "="*68 + "+")
    print("|" + " "*15 + "SAGAAGENT VERIFICATION SUITE" + " "*25 + "|")
    print("+" + "="*68 + "+")
    print()
    
    results = []
    
    # Run verifications
    results.append(("Imports", verify_imports()))
    results.append(("Configuration", verify_config()))
    results.append(("Export Service", verify_export_service()))
    
    # Summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{name:30s}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("="*70)
    if all_passed:
        print("[SUCCESS] ALL VERIFICATIONS PASSED!")
        print("SagaAgent is ready to use with ArcueAgent-style architecture!")
    else:
        print("[WARNING] SOME VERIFICATIONS FAILED")
        print("Please check the errors above and fix any issues.")
    print("="*70)
    
    return all_passed


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)

