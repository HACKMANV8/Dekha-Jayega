"""
Export Service for handling JSON and Markdown exports in SagaAgent.
Centralizes all export logic for saga components.
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Any
from SagaAgent.config import ExportConfig


class ExportService:
    """Service for exporting saga data to various formats"""
    
    @staticmethod
    def _ensure_export_dir() -> str:
        """Ensure export directory exists and return path"""
        os.makedirs(ExportConfig.EXPORT_DIR, exist_ok=True)
        return ExportConfig.EXPORT_DIR
    
    @staticmethod
    def _get_filename_base(state: dict) -> tuple[str, str]:
        """Get timestamp and sanitized title for filenames"""
        import re
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        concept = state.get("concept", {})
        title = concept.get("title", "Untitled_Saga") if isinstance(concept, dict) else "Untitled_Saga"
        # Remove or replace invalid filename characters (Windows: < > : " / \ | ? *)
        title = re.sub(r'[<>:"/\\|?*]', '_', title)
        # Replace spaces with underscores
        title = title.replace(" ", "_")
        # Remove multiple consecutive underscores
        title = re.sub(r'_+', '_', title)
        # Remove leading/trailing underscores
        title = title.strip('_')
        return timestamp, title
    
    @staticmethod
    def export_stage_json(stage_name: str, data: dict, state: dict) -> str:
        """Export individual stage data to JSON"""
        export_dir = ExportService._ensure_export_dir()
        timestamp, title = ExportService._get_filename_base(state)
        
        json_filename = f"{export_dir}{title}_{stage_name}_{timestamp}.json"
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"---JSON EXPORTED: {json_filename}---")
        return json_filename
    
    @staticmethod
    def export_stage_markdown(stage_name: str, content: str, state: dict) -> str:
        """Export individual stage data to Markdown"""
        export_dir = ExportService._ensure_export_dir()
        timestamp, title = ExportService._get_filename_base(state)
        
        md_filename = f"{export_dir}{title}_{stage_name}_{timestamp}.md"
        with open(md_filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"---MARKDOWN EXPORTED: {md_filename}---")
        return md_filename
    
    @staticmethod
    def format_concept_json(state: dict) -> dict:
        """Format concept data for JSON export"""
        concept = state.get("concept", {})
        return {
            "concept": {
                "title": concept.get("title", "Untitled"),
                "genre": concept.get("genre", ""),
                "elevator_pitch": concept.get("elevator_pitch", ""),
                "core_loop": concept.get("core_loop", ""),
                "key_mechanics": concept.get("key_mechanics", ""),
                "progression": concept.get("progression", ""),
                "world_setting": concept.get("world_setting", ""),
                "art_style": concept.get("art_style", ""),
                "target_audience": concept.get("target_audience", ""),
                "monetization": concept.get("monetization", ""),
                "usp": concept.get("usp", "")
            },
            "feedback": state.get("concept_feedback", "")
        }
    
    @staticmethod
    def format_world_lore_json(state: dict) -> dict:
        """Format world lore data for JSON export"""
        world_lore = state.get("world_lore", {})
        return {
            "world_lore": {
                "world_name": world_lore.get("world_name", "Unknown World"),
                "setting_overview": world_lore.get("setting_overview", ""),
                # Physical World
                "geography": world_lore.get("geography", ""),
                "climate_cosmology": world_lore.get("climate_cosmology", ""),
                "flora_fauna": world_lore.get("flora_fauna", ""),
                # History & Timeline
                "creation_myth": world_lore.get("creation_myth", ""),
                "historical_eras": world_lore.get("historical_eras", ""),
                "current_age": world_lore.get("current_age", ""),
                # Cultural & Social
                "civilizations": world_lore.get("civilizations", ""),
                "social_structures": world_lore.get("social_structures", ""),
                "religions_beliefs": world_lore.get("religions_beliefs", ""),
                # Systems & Mechanics
                "magic_or_technology": world_lore.get("magic_or_technology", ""),
                "economy_resources": world_lore.get("economy_resources", ""),
                "conflicts_tensions": world_lore.get("conflicts_tensions", ""),
                # Narrative Hooks
                "mysteries_legends": world_lore.get("mysteries_legends", ""),
                "story_potential": world_lore.get("story_potential", "")
            }
        }
    
    @staticmethod
    def format_factions_json(state: dict) -> dict:
        """Format factions data for JSON export"""
        return {
            "factions": [
                {
                    "faction_name": faction.get("faction_name", "Unknown Faction"),
                    "motto_tagline": faction.get("motto_tagline", ""),
                    "faction_type": faction.get("faction_type", ""),
                    "core_ideology": faction.get("core_ideology", ""),
                    "aesthetic_identity": faction.get("aesthetic_identity", ""),
                    "leader_profile": faction.get("leader_profile", ""),
                    "hierarchy": faction.get("hierarchy", ""),
                    "notable_npcs": faction.get("notable_npcs", ""),
                    "organizational_culture": faction.get("organizational_culture", ""),
                    "headquarters": faction.get("headquarters", ""),
                    "controlled_regions": faction.get("controlled_regions", ""),
                    "military_strength": faction.get("military_strength", ""),
                    "economic_power": faction.get("economic_power", ""),
                    "joining_requirements": faction.get("joining_requirements", ""),
                    "reputation_system": faction.get("reputation_system", ""),
                    "exclusive_benefits": faction.get("exclusive_benefits", ""),
                    "rank_progression": faction.get("rank_progression", ""),
                    "faction_questline": faction.get("faction_questline", ""),
                    "repeatable_activities": faction.get("repeatable_activities", ""),
                    "moral_dilemmas": faction.get("moral_dilemmas", ""),
                    "betrayal_consequences": faction.get("betrayal_consequences", ""),
                    "allied_factions": faction.get("allied_factions", ""),
                    "rival_factions": faction.get("rival_factions", ""),
                    "neutral_factions": faction.get("neutral_factions", ""),
                    "faction_war_mechanics": faction.get("faction_war_mechanics", "")
                }
                for faction in state.get("factions", [])
            ]
        }
    
    @staticmethod
    def format_characters_json(state: dict) -> dict:
        """Format characters data for JSON export"""
        return {
            "characters": [
                {
                    "character_name": char.get("character_name", "Unknown"),
                    "character_type": char.get("character_type", "NPC"),
                    "role_purpose": char.get("role_purpose", ""),
                    "tagline_quote": char.get("tagline_quote", ""),
                    "appearance": char.get("appearance", ""),
                    "silhouette_design": char.get("silhouette_design", ""),
                    "costume_design": char.get("costume_design", ""),
                    "visual_themes": char.get("visual_themes", ""),
                    "personality_traits": char.get("personality_traits", ""),
                    "motivations": char.get("motivations", ""),
                    "moral_alignment": char.get("moral_alignment", ""),
                    "character_arc": char.get("character_arc", ""),
                    "quirks_mannerisms": char.get("quirks_mannerisms", ""),
                    "backstory": char.get("backstory", ""),
                    "relationships": char.get("relationships", ""),
                    "secrets_reveals": char.get("secrets_reveals", ""),
                    "combat_style": char.get("combat_style", ""),
                    "class_abilities": char.get("class_abilities", ""),
                    "stats_attributes": char.get("stats_attributes", ""),
                    "playstyle_identity": char.get("playstyle_identity", ""),
                    "recruitment_conditions": char.get("recruitment_conditions", ""),
                    "dialogue_system": char.get("dialogue_system", ""),
                    "companion_mechanics": char.get("companion_mechanics", ""),
                    "romance_friendship": char.get("romance_friendship", "")
                }
                for char in state.get("characters", [])
            ]
        }
    
    @staticmethod
    def format_plot_arcs_json(state: dict) -> dict:
        """Format plot arcs data for JSON export"""
        return {
            "plot_arcs": [
                {
                    "arc_title": arc.get("arc_title", "Untitled Arc"),
                    "arc_type": arc.get("arc_type", ""),
                    "central_question": arc.get("central_question", ""),
                    "theme": arc.get("theme", ""),
                    "estimated_playtime": arc.get("estimated_playtime", ""),
                    # Act 1
                    "act1_hook": arc.get("act1_hook", ""),
                    "act1_worldbuilding": arc.get("act1_worldbuilding", ""),
                    "act1_tutorial": arc.get("act1_tutorial", ""),
                    "inciting_incident": arc.get("inciting_incident", ""),
                    "act1_player_goal": arc.get("act1_player_goal", ""),
                    "plot_point_1": arc.get("plot_point_1", ""),
                    # Act 2
                    "act2_progression": arc.get("act2_progression", ""),
                    "act2_complications": arc.get("act2_complications", ""),
                    "midpoint_twist": arc.get("midpoint_twist", ""),
                    "act2_setbacks": arc.get("act2_setbacks", ""),
                    "companion_development": arc.get("companion_development", ""),
                    "plot_point_2": arc.get("plot_point_2", ""),
                    # Act 3
                    "act3_final_prep": arc.get("act3_final_prep", ""),
                    "climax_sequence": arc.get("climax_sequence", ""),
                    "boss_mechanics": arc.get("boss_mechanics", ""),
                    "resolution": arc.get("resolution", ""),
                    "epilogue": arc.get("epilogue", ""),
                    # Branching
                    "major_choice_points": arc.get("major_choice_points", ""),
                    "choice_consequences": arc.get("choice_consequences", ""),
                    "conditional_content": arc.get("conditional_content", ""),
                    "multiple_endings": arc.get("multiple_endings", "")
                }
                for arc in state.get("plot_arcs", [])
            ]
        }
    
    @staticmethod
    def format_questlines_json(state: dict) -> dict:
        """Format questlines data for JSON export"""
        return {
            "questlines": [
                {
                    "quest_name": quest.get("quest_name", "Untitled Quest"),
                    "quest_type": quest.get("quest_type", ""),
                    "difficulty": quest.get("difficulty", ""),
                    "estimated_time": quest.get("estimated_time", ""),
                    # Discovery
                    "discovery_method": quest.get("discovery_method", ""),
                    "quest_giver": quest.get("quest_giver", ""),
                    "hook_pitch": quest.get("hook_pitch", ""),
                    "urgency_factor": quest.get("urgency_factor", ""),
                    # Objectives
                    "primary_objectives": quest.get("primary_objectives", ""),
                    "optional_objectives": quest.get("optional_objectives", ""),
                    "nested_objectives": quest.get("nested_objectives", ""),
                    "failure_conditions": quest.get("failure_conditions", ""),
                    # Branching
                    "choice_points": quest.get("choice_points", ""),
                    "path_outcomes": quest.get("path_outcomes", ""),
                    "skill_checks": quest.get("skill_checks", ""),
                    "faction_variations": quest.get("faction_variations", ""),
                    # Gameplay
                    "mechanics_introduced": quest.get("mechanics_introduced", ""),
                    "combat_encounters": quest.get("combat_encounters", ""),
                    "puzzle_elements": quest.get("puzzle_elements", ""),
                    "exploration_required": quest.get("exploration_required", ""),
                    # Narrative
                    "story_beats": quest.get("story_beats", ""),
                    "npc_interactions": quest.get("npc_interactions", ""),
                    "environmental_storytelling": quest.get("environmental_storytelling", ""),
                    "lore_reveals": quest.get("lore_reveals", ""),
                    # Rewards
                    "reward_structure": quest.get("reward_structure", ""),
                    "reputation_changes": quest.get("reputation_changes", ""),
                    "unlocks_consequences": quest.get("unlocks_consequences", "")
                }
                for quest in state.get("questlines", [])
            ]
        }
    
    @staticmethod
    def export_all_json(state: dict) -> dict:
        """Export all stages to JSON files"""
        print("\n---NODE: EXPORTING TO JSON---")
        
        # Validate state has required content
        if not state.get("concept"):
            print("WARNING: State has no concept - skipping export to avoid empty files")
            return {"export_path": ExportConfig.EXPORT_DIR, "export_timestamp": "", "json_files": []}
        
        export_dir = ExportService._ensure_export_dir()
        timestamp, _ = ExportService._get_filename_base(state)
        json_files = []
        
        # Export each stage if present
        if state.get("concept"):
            json_files.append(ExportService.export_stage_json("concept", ExportService.format_concept_json(state), state))
        if state.get("world_lore"):
            json_files.append(ExportService.export_stage_json("world_lore", ExportService.format_world_lore_json(state), state))
        if state.get("factions"):
            json_files.append(ExportService.export_stage_json("factions", ExportService.format_factions_json(state), state))
        if state.get("characters"):
            json_files.append(ExportService.export_stage_json("characters", ExportService.format_characters_json(state), state))
        if state.get("plot_arcs"):
            json_files.append(ExportService.export_stage_json("plot_arcs", ExportService.format_plot_arcs_json(state), state))
        if state.get("questlines"):
            json_files.append(ExportService.export_stage_json("questlines", ExportService.format_questlines_json(state), state))
        
        print(f"---ALL JSON FILES EXPORTED TO: {export_dir}---")
        print(f"Exported {len(json_files)} JSON files")
        
        return {"export_path": export_dir, "export_timestamp": timestamp, "json_files": json_files}
    
    @staticmethod
    def format_concept_markdown(state: dict) -> str:
        """Format concept as markdown"""
        concept = state.get('concept', {})
        return f"""# {concept.get('title', 'Untitled Saga')}

**Genre:** {concept.get('genre', 'TBD')}

## Elevator Pitch
{concept.get('elevator_pitch', 'TBD')}

## Core Loop
{concept.get('core_loop', 'TBD')}

## Key Mechanics
{concept.get('key_mechanics', 'TBD')}

## Progression
{concept.get('progression', 'TBD')}

## World Setting
{concept.get('world_setting', 'TBD')}

## Art Style
{concept.get('art_style', 'TBD')}

## Target Audience
{concept.get('target_audience', 'TBD')}

## Monetization
{concept.get('monetization', 'TBD')}

## Unique Selling Proposition
{concept.get('usp', 'TBD')}
"""
    
    @staticmethod
    def format_world_lore_markdown(state: dict) -> str:
        """Format world lore as markdown"""
        world_lore = state.get('world_lore', {})
        content = f"# World Lore - {world_lore.get('world_name', 'Unknown World')}\n\n"
        
        # Setting Overview
        if world_lore.get('setting_overview'):
            content += f"## Setting Overview\n{world_lore.get('setting_overview')}\n\n"
        
        # Physical World
        content += "## Physical World\n\n"
        if world_lore.get('geography'):
            content += f"### Geography\n{world_lore.get('geography')}\n\n"
        if world_lore.get('climate_cosmology'):
            content += f"### Climate & Cosmology\n{world_lore.get('climate_cosmology')}\n\n"
        if world_lore.get('flora_fauna'):
            content += f"### Flora & Fauna\n{world_lore.get('flora_fauna')}\n\n"
        
        # History & Timeline
        content += "## History & Timeline\n\n"
        if world_lore.get('creation_myth'):
            content += f"### Creation Myth\n{world_lore.get('creation_myth')}\n\n"
        if world_lore.get('historical_eras'):
            content += f"### Historical Eras\n{world_lore.get('historical_eras')}\n\n"
        if world_lore.get('current_age'):
            content += f"### Current Age\n{world_lore.get('current_age')}\n\n"
        
        # Cultural & Social
        content += "## Cultural & Social\n\n"
        if world_lore.get('civilizations'):
            content += f"### Civilizations\n{world_lore.get('civilizations')}\n\n"
        if world_lore.get('social_structures'):
            content += f"### Social Structures\n{world_lore.get('social_structures')}\n\n"
        if world_lore.get('religions_beliefs'):
            content += f"### Religions & Beliefs\n{world_lore.get('religions_beliefs')}\n\n"
        
        # Systems & Mechanics
        content += "## Systems & Mechanics\n\n"
        if world_lore.get('magic_or_technology'):
            content += f"### Magic/Technology\n{world_lore.get('magic_or_technology')}\n\n"
        if world_lore.get('economy_resources'):
            content += f"### Economy & Resources\n{world_lore.get('economy_resources')}\n\n"
        if world_lore.get('conflicts_tensions'):
            content += f"### Conflicts & Tensions\n{world_lore.get('conflicts_tensions')}\n\n"
        
        # Narrative Hooks
        content += "## Narrative Hooks\n\n"
        if world_lore.get('mysteries_legends'):
            content += f"### Mysteries & Legends\n{world_lore.get('mysteries_legends')}\n\n"
        if world_lore.get('story_potential'):
            content += f"### Story Potential\n{world_lore.get('story_potential')}\n\n"
        
        return content
    
    @staticmethod
    def format_factions_markdown(state: dict) -> str:
        """Format factions as markdown"""
        concept = state.get('concept', {})
        title = concept.get('title', 'Untitled Saga') if isinstance(concept, dict) else 'Untitled Saga'
        content = f"# Factions - {title}\n\n"
        
        for i, faction in enumerate(state.get('factions', []), 1):
            content += f"## {i}. {faction.get('faction_name', 'Unknown Faction')}\n\n"
            
            if faction.get('motto_tagline'):
                content += f"**Motto:** \"{faction.get('motto_tagline')}\"\n\n"
            
            if faction.get('faction_type'):
                content += f"**Type:** {faction.get('faction_type')}  \n"
            if faction.get('core_ideology'):
                content += f"**Ideology:** {faction.get('core_ideology')}  \n\n"
            
            if faction.get('leader_profile'):
                content += f"### Leadership\n{faction.get('leader_profile')}\n\n"
            
            if faction.get('hierarchy'):
                content += f"### Hierarchy\n{faction.get('hierarchy')}\n\n"
            
            if faction.get('headquarters'):
                content += f"### Headquarters\n{faction.get('headquarters')}\n\n"
            
            if faction.get('controlled_regions'):
                content += f"### Territory\n{faction.get('controlled_regions')}\n\n"
            
            if faction.get('military_strength'):
                content += f"### Military Strength\n{faction.get('military_strength')}\n\n"
            
            if faction.get('economic_power'):
                content += f"### Economic Power\n{faction.get('economic_power')}\n\n"
            
            if faction.get('joining_requirements'):
                content += f"### Joining\n{faction.get('joining_requirements')}\n\n"
            
            if faction.get('faction_questline'):
                content += f"### Main Questline\n{faction.get('faction_questline')}\n\n"
            
            if faction.get('allied_factions'):
                content += f"**Allies:** {faction.get('allied_factions')}  \n"
            if faction.get('rival_factions'):
                content += f"**Rivals:** {faction.get('rival_factions')}  \n\n"
            
            content += "---\n\n"
        
        return content
    
    @staticmethod
    def format_characters_markdown(state: dict) -> str:
        """Format characters as markdown"""
        concept = state.get('concept', {})
        title = concept.get('title', 'Untitled Saga') if isinstance(concept, dict) else 'Untitled Saga'
        content = f"# Characters - {title}\n\n"
        
        for i, char in enumerate(state.get('characters', []), 1):
            content += f"## {i}. {char.get('character_name', 'Unknown')}\n\n"
            
            if char.get('tagline_quote'):
                content += f"_{char.get('tagline_quote')}_\n\n"
            
            if char.get('character_type'):
                content += f"**Type:** {char.get('character_type')}  \n"
            if char.get('role_purpose'):
                content += f"**Role:** {char.get('role_purpose')}  \n\n"
            
            # Visual Design
            content += "### Visual Design\n\n"
            if char.get('appearance'):
                content += f"**Appearance:** {char.get('appearance')}\n\n"
            if char.get('costume_design'):
                content += f"**Costume:** {char.get('costume_design')}\n\n"
            
            # Personality & Psychology
            if char.get('personality_traits'):
                content += f"### Personality\n{char.get('personality_traits')}\n\n"
            if char.get('motivations'):
                content += f"### Motivations\n{char.get('motivations')}\n\n"
            if char.get('moral_alignment'):
                content += f"**Moral Alignment:** {char.get('moral_alignment')}\n\n"
            
            # Background
            if char.get('backstory'):
                content += f"### Backstory\n{char.get('backstory')}\n\n"
            if char.get('relationships'):
                content += f"### Relationships\n{char.get('relationships')}\n\n"
            
            # Gameplay
            if char.get('combat_style'):
                content += f"### Combat Style\n{char.get('combat_style')}\n\n"
            if char.get('class_abilities'):
                content += f"### Abilities\n{char.get('class_abilities')}\n\n"
            
            content += "---\n\n"
        
        return content
    
    @staticmethod
    def format_plot_arcs_markdown(state: dict) -> str:
        """Format plot arcs as markdown"""
        concept = state.get('concept', {})
        title = concept.get('title', 'Untitled Saga') if isinstance(concept, dict) else 'Untitled Saga'
        content = f"# Plot Arcs - {title}\n\n"
        
        for i, arc in enumerate(state.get('plot_arcs', []), 1):
            content += f"## {i}. {arc.get('arc_title', 'Untitled Arc')}\n\n"
            
            if arc.get('arc_type'):
                content += f"**Type:** {arc.get('arc_type')}  \n"
            if arc.get('theme'):
                content += f"**Theme:** {arc.get('theme')}  \n"
            if arc.get('estimated_playtime'):
                content += f"**Playtime:** {arc.get('estimated_playtime')}  \n\n"
            
            if arc.get('central_question'):
                content += f"### Central Question\n{arc.get('central_question')}\n\n"
            
            # Act 1
            content += "### Act 1: Setup\n\n"
            if arc.get('act1_hook'):
                content += f"**Hook:** {arc.get('act1_hook')}\n\n"
            if arc.get('inciting_incident'):
                content += f"**Inciting Incident:** {arc.get('inciting_incident')}\n\n"
            
            # Act 2
            content += "### Act 2: Confrontation\n\n"
            if arc.get('midpoint_twist'):
                content += f"**Midpoint Twist:** {arc.get('midpoint_twist')}\n\n"
            if arc.get('act2_setbacks'):
                content += f"**Setbacks:** {arc.get('act2_setbacks')}\n\n"
            
            # Act 3
            content += "### Act 3: Resolution\n\n"
            if arc.get('climax_sequence'):
                content += f"**Climax:** {arc.get('climax_sequence')}\n\n"
            if arc.get('resolution'):
                content += f"**Resolution:** {arc.get('resolution')}\n\n"
            
            if arc.get('multiple_endings'):
                content += f"### Multiple Endings\n{arc.get('multiple_endings')}\n\n"
            
            content += "---\n\n"
        
        return content
    
    @staticmethod
    def format_questlines_markdown(state: dict) -> str:
        """Format questlines as markdown"""
        concept = state.get('concept', {})
        title = concept.get('title', 'Untitled Saga') if isinstance(concept, dict) else 'Untitled Saga'
        content = f"# Questlines - {title}\n\n"
        
        for i, quest in enumerate(state.get('questlines', []), 1):
            content += f"## {i}. {quest.get('quest_name', 'Untitled Quest')}\n\n"
            
            if quest.get('quest_type'):
                content += f"**Type:** {quest.get('quest_type')}  \n"
            if quest.get('difficulty'):
                content += f"**Difficulty:** {quest.get('difficulty')}  \n"
            if quest.get('estimated_time'):
                content += f"**Time:** {quest.get('estimated_time')}  \n\n"
            
            if quest.get('hook_pitch'):
                content += f"### Hook\n{quest.get('hook_pitch')}\n\n"
            
            if quest.get('quest_giver'):
                content += f"**Quest Giver:** {quest.get('quest_giver')}  \n\n"
            
            if quest.get('primary_objectives'):
                content += f"### Objectives\n{quest.get('primary_objectives')}\n\n"
            
            if quest.get('choice_points'):
                content += f"### Choices\n{quest.get('choice_points')}\n\n"
            
            if quest.get('reward_structure'):
                content += f"### Rewards\n{quest.get('reward_structure')}\n\n"
            
            if quest.get('unlocks_consequences'):
                content += f"### Unlocks\n{quest.get('unlocks_consequences')}\n\n"
            
            content += "---\n\n"
        
        return content
    
    @staticmethod
    def export_all_markdown(state: dict) -> dict:
        """Export all stages to Markdown files"""
        print("\n---NODE: EXPORTING TO MARKDOWN---")
        
        # Validate state has required content
        if not state.get("concept"):
            print("WARNING: State has no concept - skipping markdown export to avoid empty files")
            return {"markdown_files": []}
        
        export_dir = ExportService._ensure_export_dir()
        timestamp, _ = ExportService._get_filename_base(state)
        md_files = []
        
        # Export each stage if present
        if state.get("concept"):
            md_files.append(ExportService.export_stage_markdown("concept", ExportService.format_concept_markdown(state), state))
        if state.get("world_lore"):
            md_files.append(ExportService.export_stage_markdown("world_lore", ExportService.format_world_lore_markdown(state), state))
        if state.get("factions"):
            md_files.append(ExportService.export_stage_markdown("factions", ExportService.format_factions_markdown(state), state))
        if state.get("characters"):
            md_files.append(ExportService.export_stage_markdown("characters", ExportService.format_characters_markdown(state), state))
        if state.get("plot_arcs"):
            md_files.append(ExportService.export_stage_markdown("plot_arcs", ExportService.format_plot_arcs_markdown(state), state))
        if state.get("questlines"):
            md_files.append(ExportService.export_stage_markdown("questlines", ExportService.format_questlines_markdown(state), state))
        
        print(f"---ALL MARKDOWN FILES EXPORTED TO: {export_dir}---")
        print(f"Exported {len(md_files)} Markdown files")
        
        return {"markdown_files": md_files}

