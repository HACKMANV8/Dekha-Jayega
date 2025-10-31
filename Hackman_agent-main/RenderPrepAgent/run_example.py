#!/usr/bin/env python3
"""
Example script demonstrating RenderPrepAgent usage.

This script shows how to use RenderPrepAgent programmatically
to generate image prompts from saga data.
"""
import os
import sys
import json
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from RenderPrepAgent.agent import run_render_prep, load_saga_data
from RenderPrepAgent.config import AgentConfig


def create_example_saga_data() -> Dict[str, Any]:
    """
    Create example saga data for demonstration.
    
    In real usage, this would come from SagaAgent output.
    """
    return {
        "concept": {
            "title": "Echoes of Eternity",
            "genre": "Fantasy RPG",
            "art_style": "fantasy",
            "elevator_pitch": "A tale of ancient magic and forgotten kingdoms"
        },
        "world_lore": {
            "world_name": "Aethoria",
            "geography": "Vast continent with floating islands, ancient forests, and crystal mountains. "
                        "The land is scarred by the Cataclysm, with reality-bending anomalies scattered across regions.",
            "setting_overview": "A world where magic has returned after centuries of dormancy",
            "civilizations": "Great city of Lumina built around an ancient magical spire"
        },
        "characters": [
            {
                "character_name": "Elara Moonwhisper",
                "character_type": "Protagonist",
                "appearance": "Silver-haired elf mage with luminous emerald eyes. Wears flowing midnight blue robes "
                             "adorned with constellation patterns that shimmer with starlight. Carries an ancient oak staff "
                             "topped with a glowing moonstone crystal.",
                "silhouette_design": "Elegant standing pose with staff, robes flowing in ethereal wind",
                "visual_themes": "Blues, silvers, starlight, mystical aura",
                "personality_traits": "Wise, mysterious, compassionate",
                "role_purpose": "The last guardian of ancient magical knowledge",
                "backstory": "Once a keeper of the Sacred Grove, now seeking to prevent the return of dark forces"
            },
            {
                "character_name": "Kael Ironheart",
                "character_type": "Companion",
                "appearance": "Battle-scarred human warrior with short black hair and steel-gray eyes. "
                             "Wears weathered plate armor with a crimson lion emblem. Wields the legendary "
                             "greatsword 'Oathkeeper' which glows with golden runes when drawn.",
                "silhouette_design": "Heroic stance with sword, cape billowing",
                "visual_themes": "Reds, golds, steel, valor and honor",
                "personality_traits": "Brave, loyal, honorable",
                "role_purpose": "Sworn protector and veteran soldier",
                "backstory": "Former captain of the King's Guard, seeking redemption for past failures",
                "combat_style": "Two-handed greatsword combat, defensive formations"
            }
        ],
        "factions": [
            {
                "faction_name": "Order of the Dawn",
                "faction_type": "Holy Order",
                "aesthetic_identity": "White and gold, radiant light, divine symbols",
                "headquarters": "The Radiant Spire - a towering cathedral of white marble and golden spires, "
                               "built on a floating island. Stained glass windows depict ancient legends. "
                               "The central chamber houses the Eternal Flame.",
                "core_ideology": "Protect the realm from darkness through divine light"
            }
        ],
        "plot_arcs": [
            {
                "arc_title": "The Awakening",
                "arc_type": "Main Story",
                "theme": "Discovery and destiny",
                "central_question": "Can the ancient Shard of Eternity be recovered before dark forces claim it?",
                "act1_hook": "The protagonist discovers a mysterious magical artifact in the ruins of an ancient temple, "
                            "triggering visions of an impending catastrophe",
                "midpoint_twist": "The artifact reveals it is one of seven Shards scattered across the world, "
                                 "and dark forces have already claimed three",
                "climax_sequence": "Epic battle at the Nexus of Realms as heroes confront the Shadow Lord "
                                  "attempting to merge all Shards and rewrite reality",
                "epilogue": "The world is saved but forever changed, with new magical balance established"
            }
        ],
        "questlines": []
    }


def main():
    """Main example execution."""
    print("="*70)
    print("RENDERPREPAGENT - EXAMPLE USAGE")
    print("="*70)
    
    # Option 1: Create example data
    print("\n[Option 1] Using example saga data...")
    saga_data = create_example_saga_data()
    
    # Option 2: Load from file (if available)
    # Uncomment to use:
    # print("\n[Option 2] Loading saga data from file...")
    # saga_data = load_saga_data("./saga_exports/your_saga.json")
    
    # Configure agent
    print("\nConfiguring RenderPrepAgent...")
    config = AgentConfig(
        thread_id="example_run",
        quality_preset="standard",  # Try: "draft", "standard", "premium"
        generate_images=False,       # Set to True if you have Nano Banana API key
        auto_continue=True
    )
    
    print(f"  - Quality Preset: {config.quality_preset}")
    print(f"  - Generate Images: {config.generate_images}")
    
    # Run render prep
    print("\n" + "="*70)
    print("STARTING RENDER PREP WORKFLOW")
    print("="*70)
    
    result = run_render_prep(saga_data, config)
    
    # Display results
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    
    print(f"\n✓ Character Prompts: {len(result.get('character_prompts', []))}")
    for i, char in enumerate(result.get('character_prompts', [])[:2], 1):  # Show first 2
        print(f"\n  {i}. {char['name']} ({char['type']})")
        print(f"     Positive: {char['positive_prompt'][:100]}...")
        print(f"     Negative: {char['negative_prompt'][:80]}...")
    
    print(f"\n✓ Environment Prompts: {len(result.get('environment_prompts', []))}")
    for i, env in enumerate(result.get('environment_prompts', [])[:1], 1):  # Show first 1
        print(f"\n  {i}. {env['name']}")
        print(f"     Positive: {env['positive_prompt'][:100]}...")
    
    print(f"\n✓ Item Prompts: {len(result.get('item_prompts', []))}")
    print(f"✓ Storyboard Prompts: {len(result.get('storyboard_prompts', []))}")
    
    # Export info
    export_path = result.get('export_path', './saga_exports/renders/')
    print(f"\n📁 All prompts exported to: {export_path}")
    
    json_files = result.get('json_files', [])
    md_files = result.get('markdown_files', [])
    
    if json_files:
        print(f"\n📄 JSON files ({len(json_files)}):")
        for f in json_files[:3]:  # Show first 3
            print(f"  - {os.path.basename(f)}")
    
    if md_files:
        print(f"\n📝 Markdown files ({len(md_files)}):")
        for f in md_files[:3]:  # Show first 3
            print(f"  - {os.path.basename(f)}")
    
    # Show how to use the prompts
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("\n1. Check the exported Markdown files for human-readable prompts")
    print("2. Copy prompts to your image generator (Nano Banana, Stable Diffusion, etc.)")
    print("3. Or set NANO_BANANA_API_KEY and use --generate-images to auto-generate")
    
    print("\nExample command with API:")
    print("  export NANO_BANANA_API_KEY='your_key'")
    print("  python -m RenderPrepAgent.agent ./saga_exports/ --generate-images")
    
    print("\n" + "="*70)
    print("EXAMPLE COMPLETE ✓")
    print("="*70)


if __name__ == "__main__":
    main()

