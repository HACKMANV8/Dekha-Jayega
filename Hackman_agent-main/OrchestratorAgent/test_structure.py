#!/usr/bin/env python3
"""
Test script to verify orchestrator structure and imports.
This doesn't require API keys - it just validates the structure.
"""

import sys
import os

# Add project root to path (parent of OrchestratorAgent)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def test_imports():
    """Test that all orchestrator components can be imported"""
    print("Testing imports...")
    
    try:
        from OrchestratorAgent.models.orchestrator import (
            ComponentFeedback,
            UserViewAnalysis,
            RevisionPlan
        )
        print("[OK] Models imported successfully")
    except Exception as e:
        print(f"[FAIL] Failed to import models: {e}")
        return False
    
    try:
        from OrchestratorAgent.prompts.orchestrator_prompts import (
            get_user_view_analysis_prompt,
            get_revision_plan_prompt
        )
        print("[OK] Prompts imported successfully")
    except Exception as e:
        print(f"[FAIL] Failed to import prompts: {e}")
        return False
    
    try:
        from OrchestratorAgent.orchestrator import OrchestratorAgent
        print("[OK] Orchestrator agent imported successfully")
    except Exception as e:
        print(f"[FAIL] Failed to import orchestrator: {e}")
        return False
    
    return True


def test_model_structure():
    """Test that orchestrator models have correct structure"""
    print("\nTesting model structure...")
    
    from OrchestratorAgent.models.orchestrator import (
        ComponentFeedback,
        UserViewAnalysis,
        RevisionPlan
    )
    
    # Test ComponentFeedback
    try:
        cf = ComponentFeedback(
            component_name="draft",
            needs_update=True,
            feedback="Test feedback",
            priority=1
        )
        print(f"[OK] ComponentFeedback created: {cf.component_name}")
    except Exception as e:
        print(f"[FAIL] Failed to create ComponentFeedback: {e}")
        return False
    
    # Test UserViewAnalysis
    try:
        analysis = UserViewAnalysis(
            overall_assessment="Test assessment",
            story_coherence_score=8,
            component_feedback=[cf],
            suggested_improvements=["Improvement 1", "Improvement 2"]
        )
        print(f"[OK] UserViewAnalysis created: score={analysis.story_coherence_score}")
        
        # Test helper methods
        components = analysis.get_components_to_update()
        print(f"[OK] get_components_to_update() works: {components}")
        
        feedback = analysis.get_feedback_for_component("draft")
        print(f"[OK] get_feedback_for_component() works: {feedback[:50]}...")
    except Exception as e:
        print(f"[FAIL] Failed to create UserViewAnalysis: {e}")
        return False
    
    # Test RevisionPlan
    try:
        plan = RevisionPlan(
            revision_summary="Test revision",
            components_to_update=["draft", "characters"],
            update_strategy="sequential",
            estimated_impact="High impact"
        )
        print(f"[OK] RevisionPlan created: {len(plan.components_to_update)} components")
    except Exception as e:
        print(f"[FAIL] Failed to create RevisionPlan: {e}")
        return False
    
    return True


def test_orchestrator_methods():
    """Test that orchestrator has required methods"""
    print("\nTesting orchestrator methods...")
    
    from OrchestratorAgent.orchestrator import OrchestratorAgent
    
    # Check methods exist
    required_methods = [
        'load_user_view',
        'analyze_user_view',
        'update_state_from_user_view',
        'update_component',
        'compile_and_export',
        'orchestrate_revision',
        'interactive_revision'
    ]
    
    for method in required_methods:
        if hasattr(OrchestratorAgent, method):
            print(f"[OK] Method exists: {method}")
        else:
            print(f"[FAIL] Method missing: {method}")
            return False
    
    return True


def test_prompt_generation():
    """Test that prompts can be generated"""
    print("\nTesting prompt generation...")
    
    from OrchestratorAgent.prompts.orchestrator_prompts import (
        get_user_view_analysis_prompt,
        get_revision_plan_prompt
    )
    
    # Test analysis prompt
    try:
        test_data = {
            'title': 'Test Story',
            'genre': 'Test Genre',
            'tone': 'Test Tone',
            'log_line': 'Test log line',
            'draft': 'Test draft',
            'visual_style': {},
            'characters': [],
            'dialogues_by_character': {},
            'locations': [],
            'scenes': []
        }
        
        prompt = get_user_view_analysis_prompt(test_data)
        print(f"[OK] Analysis prompt generated: {len(prompt)} chars")
        
        # Verify prompt contains key elements
        if 'Test Story' in prompt and 'Test Genre' in prompt:
            print("[OK] Prompt contains user_view data")
        else:
            print("[FAIL] Prompt missing user_view data")
            return False
            
    except Exception as e:
        print(f"[FAIL] Failed to generate analysis prompt: {e}")
        return False
    
    # Test revision plan prompt
    try:
        test_analysis = {
            'overall_assessment': 'Test assessment',
            'story_coherence_score': 8,
            'component_feedback': [],
            'suggested_improvements': []
        }
        
        prompt = get_revision_plan_prompt(test_analysis)
        print(f"[OK] Revision plan prompt generated: {len(prompt)} chars")
    except Exception as e:
        print(f"[FAIL] Failed to generate revision plan prompt: {e}")
        return False
    
    return True


def test_file_structure():
    """Test that all required files exist"""
    print("\nTesting file structure...")
    
    files_to_check = [
        'OrchestratorAgent/orchestrator.py',
        'OrchestratorAgent/models/orchestrator.py',
        'OrchestratorAgent/prompts/orchestrator_prompts.py',
        'OrchestratorAgent/run_orchestrator.py',
        'OrchestratorAgent/README.md',
        'OrchestratorAgent/SETUP.md'
    ]
    
    for filepath in files_to_check:
        full_path = os.path.join(project_root, filepath)
        if os.path.exists(full_path):
            print(f"[OK] File exists: {filepath}")
        else:
            print(f"[FAIL] File missing: {filepath}")
            return False
    
    return True


def main():
    """Run all tests"""
    print("="*70)
    print("ORCHESTRATOR STRUCTURE TEST")
    print("="*70)
    print()
    
    all_passed = True
    
    all_passed = test_imports() and all_passed
    all_passed = test_model_structure() and all_passed
    all_passed = test_orchestrator_methods() and all_passed
    all_passed = test_prompt_generation() and all_passed
    all_passed = test_file_structure() and all_passed
    
    print()
    print("="*70)
    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED")
        print()
        print("The orchestrator is properly structured and ready to use.")
        print("To use it, set up your .env file with API keys and run:")
        print()
        print("  python3 run_orchestrator.py ArcueAgent/exports/YOUR_FILE.json")
        print()
    else:
        print("[ERROR] SOME TESTS FAILED")
        print()
        print("Please review the errors above.")
        return 1
    print("="*70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

