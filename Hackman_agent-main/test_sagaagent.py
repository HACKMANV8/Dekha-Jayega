#!/usr/bin/env python3
"""Test script to validate SagaAgent structure and imports."""

def main():
    print("="*70)
    print("SAGAAGENT VALIDATION TEST")
    print("="*70)
    
    try:
        print("\n[1] Testing imports...")
        from SagaAgent.config import AgentConfig, ExportConfig, ModelConfig
        print("    [OK] Config classes")
        
        from SagaAgent.models.concept import ConceptDoc
        from SagaAgent.models.lore import WorldLore
        from SagaAgent.models.faction import GameFaction
        from SagaAgent.models.character import GameCharacter
        from SagaAgent.models.plot import PlotArc
        from SagaAgent.models.quest import Questline
        print("    [OK] Narrative models (6 types)")
        
        from SagaAgent.models.render_prep import (
            CharacterVisualPrompt, EnvironmentPrompt, ItemPrompt, StoryboardFrame
        )
        print("    [OK] RenderPrep models (4 types)")
        
        from SagaAgent.utils.state import SagaState
        print("    [OK] SagaState")
        
        from SagaAgent.utils.llm_service import LLMService
        print("    [OK] LLMService")
        
        print("\n[2] Testing configuration...")
        config = AgentConfig.from_env()
        print(f"    [OK] AgentConfig: thread_id={config.thread_id[:8]}...")
        print(f"    [OK] Auto-continue: {config.auto_continue}")
        print(f"    [OK] Model: {config.model or 'auto-detect'}")
        
        print("\n[3] Testing model instantiation...")
        concept = ConceptDoc(
            title="Test Game",
            genre="RPG",
            elevator_pitch="A test game",
            core_loop="Play",
            key_mechanics="Combat",
            progression="Level up",
            world_setting="Fantasy world",
            art_style="Pixel art",
            target_audience="Everyone",
            monetization="Free",
            usp="Unique"
        )
        print(f"    [OK] ConceptDoc: {concept.title}")
        
        print("\n[4] Checking node imports...")
        from SagaAgent.nodes import (
            generate_concept_node,
            generate_world_lore_node,
            generate_factions_node,
            generate_characters_node,
            generate_plot_arcs_node,
            generate_questlines_node,
        )
        print("    [OK] All 6 narrative nodes")
        
        print("\n" + "="*70)
        print("[SUCCESS] ALL VALIDATION CHECKS PASSED")
        print("="*70)
        print("\nSagaAgent is ready for use!")
        print("\nQuick start:")
        print("  python -m SagaAgent.agent TOPIC=\"Your game idea\" AUTO_CONTINUE=true")
        print("\nFor interactive mode with feedback:")
        print("  python -m SagaAgent.agent TOPIC=\"Your game idea\"")
        print("="*70)
        
    except Exception as e:
        print(f"\n[FAILED] VALIDATION FAILED")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
