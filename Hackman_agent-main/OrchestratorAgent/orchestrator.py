"""
Orchestrator Agent for ArcueAgent.

This agent analyzes existing user_view files, gets LLM feedback,
and selectively updates only the components that need improvement.
"""
import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from OrchestratorAgent.models.orchestrator import UserViewAnalysis, RevisionPlan, ComponentIdentification
from OrchestratorAgent.prompts.orchestrator_prompts import (
    get_user_view_analysis_prompt,
    get_revision_plan_prompt,
    get_component_identification_prompt
)
from OrchestratorAgent.agents.react_orchestrator import ReactOrchestratorAgent
from SagaAgent.services.llm_service import LLMService
from SagaAgent.config import AgentConfig, ExportConfig

# Import node functions
from SagaAgent.nodes import (
    create_initial_draft,
    create_characters,
    create_dialogue,
    create_locations,
    define_visual_language,
    create_scenes,
    compile_script,
    export_user_view  # Only user_view export (individual component exports skipped)
)


class OrchestratorAgent:
    """
    Orchestrator agent that analyzes and revises story components.
    """
    
    def __init__(self, agent_config: Optional[AgentConfig] = None, use_react: bool = True):
        """
        Initialize the orchestrator agent.
        
        Args:
            agent_config: Optional configuration. If None, loads from environment.
            use_react: If True, use ReAct agent for reasoning. If False, use direct LLM calls.
        """
        self.config = agent_config or AgentConfig.from_env()
        self.state = self._initialize_state()
        self.use_react = use_react
    
    def _initialize_state(self) -> dict:
        """Initialize state with configuration"""
        return self.config.to_state_dict()
    
    def load_user_view(self, filepath: str) -> dict:
        """
        Load a user_view JSON file.
        
        Args:
            filepath: Path to the user_view JSON file
            
        Returns:
            The loaded user_view data as a dictionary
        """
        print(f"\n{'='*70}")
        print(f"LOADING USER VIEW FILE")
        print(f"{'='*70}")
        print(f"File: {filepath}")
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"User view file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            user_view_data = json.load(f)
        
        print(f"[OK] Loaded successfully")
        print(f"  - Title: {user_view_data.get('title', 'Unknown')}")
        print(f"  - Genre: {user_view_data.get('genre', 'Unknown')}")
        print(f"  - Characters: {len(user_view_data.get('characters', []))}")
        print(f"  - Scenes: {len(user_view_data.get('scenes', []))}")
        print(f"  - Locations: {len(user_view_data.get('locations', []))}")
        print(f"{'='*70}\n")
        
        return user_view_data
    
    def analyze_user_view(
        self, 
        user_view_data: dict, 
        user_feedback: str = ""
    ) -> UserViewAnalysis:
        """
        Analyze a user_view file using LLM and get structured feedback.
        
        Args:
            user_view_data: The user_view JSON data
            user_feedback: Optional additional feedback from the user
            
        Returns:
            Structured analysis with component feedback
        """
        print(f"\n{'='*70}")
        print(f"ANALYZING STORY WITH LLM")
        print(f"{'='*70}")
        print(f"Model: {self.state.get('model', 'default')}")
        
        if user_feedback:
            print(f"User Feedback: {user_feedback[:100]}...")
        
        # Create LLM with structured output
        llm = LLMService.create_structured_llm(
            self.state,
            UserViewAnalysis,
            creative=False  # Use analytical temperature
        )
        
        # Generate analysis prompt
        prompt = get_user_view_analysis_prompt(user_view_data, user_feedback)
        
        # Get analysis from LLM
        print("Invoking LLM for analysis...")
        analysis = llm.invoke(prompt)
        
        print(f"[OK] Analysis complete")
        print(f"  - Story Coherence Score: {analysis.story_coherence_score}/10")
        print(f"  - Components needing update: {len(analysis.get_components_to_update())}")
        print(f"{'='*70}\n")
        
        return analysis
    
    def display_analysis(self, analysis: UserViewAnalysis) -> None:
        """
        Display the analysis results in a readable format.
        
        Args:
            analysis: The UserViewAnalysis object
        """
        print(f"\n{'='*70}")
        print(f"STORY ANALYSIS RESULTS")
        print(f"{'='*70}")
        print(f"\nStory Coherence Score: {analysis.story_coherence_score}/10\n")
        
        print(f"Overall Assessment:")
        print(f"{analysis.overall_assessment}\n")
        
        print(f"Suggested Improvements:")
        for i, improvement in enumerate(analysis.suggested_improvements, 1):
            print(f"  {i}. {improvement}")
        
        print(f"\nComponent Feedback:")
        print(f"{'='*70}")
        
        for cf in analysis.component_feedback:
            status = "[WARNING] NEEDS UPDATE" if cf.needs_update else "[OK] OK"
            priority_label = {1: "[HIGH]", 2: "[MED]", 3: "[LOW]"}.get(cf.priority, "[INFO]")
            
            print(f"\n{status} {priority_label} {cf.component_name.upper()}")
            print(f"   Priority: {cf.priority}/3")
            if cf.needs_update:
                print(f"   Feedback: {cf.feedback}")
        
        print(f"\n{'='*70}\n")
    
    def update_state_from_user_view(self, user_view_data: dict) -> None:
        """
        Update internal state from user_view data to prepare for component updates.
        
        Args:
            user_view_data: The user_view JSON data
        """
        print(f"Updating state from user_view data...")
        
        # Transfer core story data
        self.state['title'] = user_view_data.get('title', 'Untitled')
        self.state['genre'] = user_view_data.get('genre', '')
        self.state['tone'] = user_view_data.get('tone', '')
        self.state['log_line'] = user_view_data.get('log_line', '')
        self.state['draft'] = user_view_data.get('draft', '')
        
        # Transfer visual style (from visual_lookbook)
        visual_style = user_view_data.get('visual_style', {})
        if visual_style:
            self.state['visual_lookbook'] = visual_style
        
        # Transfer characters
        self.state['characters'] = user_view_data.get('characters', [])
        
        # Transfer locations
        self.state['locations'] = user_view_data.get('locations', [])
        
        # Convert dialogues_by_character back to dialogue_scenes format
        dialogues_by_character = user_view_data.get('dialogues_by_character', {})
        if dialogues_by_character:
            # Create dialogue_scenes structure
            dialogue_scenes = []
            for char_name, lines in dialogues_by_character.items():
                for line_data in lines:
                    dialogue_scenes.append({
                        'character_name': char_name,
                        'scene_number': line_data.get('scene_number', 0),
                        'line': line_data.get('line', '')
                    })
            self.state['dialogue_scenes'] = dialogue_scenes
        
        # Transfer scenes
        scenes = user_view_data.get('scenes', [])
        if scenes:
            # Convert back to internal format
            internal_scenes = []
            for scene in scenes:
                visual_elements = scene.get('visual_elements', {})
                camera_work = scene.get('camera_work', {})
                
                # Convert dialogue format: user_view uses 'character', internal uses 'character_name'
                dialogues_in_scene = scene.get('dialogues_in_scene', [])
                internal_dialogue_lines = []
                for dialogue in dialogues_in_scene:
                    internal_dialogue_lines.append({
                        'character_name': dialogue.get('character', 'UNKNOWN'),  # Convert field name
                        'line': dialogue.get('line', '')
                    })
                
                internal_scene = {
                    'scene_number': scene.get('scene_number', 0),
                    'environmental_context': visual_elements.get('environmental_context', ''),
                    'subject_action': visual_elements.get('subject_action', ''),
                    'shot_type': camera_work.get('shot_type', ''),
                    'camera_angle': camera_work.get('camera_angle', ''),
                    'camera_movement': camera_work.get('camera_movement', ''),
                    'camera_perspective': camera_work.get('camera_perspective', ''),
                    'dialogue_lines': internal_dialogue_lines  # Use converted dialogue
                }
                internal_scenes.append(internal_scene)
            
            self.state['scenes'] = internal_scenes
            
            # CRITICAL: Store the current number of scenes to preserve scene count
            # This ensures the orchestrator doesn't arbitrarily increase scene count
            current_scene_count = len(internal_scenes)
            self.state['number_of_scenes'] = current_scene_count
            print(f"[INFO] Preserved scene count: {current_scene_count} scenes")
        
        print(f"[OK] State updated successfully")
    
    def _propagate_character_name_change(self, old_name: str, new_name: str) -> None:
        """
        Propagate character name changes throughout the state.
        Updates all references to the old name in dialogue, scenes, and action descriptions.
        
        Args:
            old_name: The old character name
            new_name: The new character name
        """
        updates_made = []
        
        # Update dialogue_scenes
        if 'dialogue_scenes' in self.state and self.state['dialogue_scenes']:
            dialogue_updated = 0
            for dialogue in self.state['dialogue_scenes']:
                if dialogue.get('character_name') == old_name:
                    dialogue['character_name'] = new_name
                    dialogue_updated += 1
            if dialogue_updated > 0:
                updates_made.append(f"{dialogue_updated} dialogue line(s)")
        
        # Update scenes (dialogue_lines within scenes)
        if 'scenes' in self.state and self.state['scenes']:
            scene_dialogue_updated = 0
            scene_action_updated = 0
            
            for scene in self.state['scenes']:
                # Update dialogue_lines within scenes
                if 'dialogue_lines' in scene and scene['dialogue_lines']:
                    for dialogue_line in scene['dialogue_lines']:
                        if dialogue_line.get('character_name') == old_name:
                            dialogue_line['character_name'] = new_name
                            scene_dialogue_updated += 1
                
                # Get first name for more natural replacement
                old_first_name = old_name.split()[0] if ' ' in old_name else old_name
                new_first_name = new_name.split()[0] if ' ' in new_name else new_name
                
                # Update character name in subject_action (scene descriptions)
                if 'subject_action' in scene and scene['subject_action']:
                    subject_action = scene['subject_action']
                    updated_action = subject_action
                    
                    # Replace full name first, then first name
                    if old_name in updated_action:
                        updated_action = updated_action.replace(old_name, new_name)
                        scene_action_updated += 1
                    elif old_first_name != old_name and old_first_name in updated_action:
                        updated_action = updated_action.replace(old_first_name, new_first_name)
                        scene_action_updated += 1
                    
                    if updated_action != subject_action:
                        scene['subject_action'] = updated_action
                
                # Update character name in environmental_context as well
                if 'environmental_context' in scene and scene['environmental_context']:
                    env_context = scene['environmental_context']
                    updated_context = env_context
                    
                    # Replace full name first, then first name
                    if old_name in updated_context:
                        updated_context = updated_context.replace(old_name, new_name)
                        scene_action_updated += 1
                    elif old_first_name != old_name and old_first_name in updated_context:
                        updated_context = updated_context.replace(old_first_name, new_first_name)
                        scene_action_updated += 1
                    
                    if updated_context != env_context:
                        scene['environmental_context'] = updated_context
            
            if scene_dialogue_updated > 0:
                updates_made.append(f"{scene_dialogue_updated} scene dialogue(s)")
            if scene_action_updated > 0:
                updates_made.append(f"{scene_action_updated} scene action(s)")
        
        # Update draft/story text
        if 'draft' in self.state and self.state['draft']:
            draft = self.state['draft']
            old_first_name = old_name.split()[0] if ' ' in old_name else old_name
            new_first_name = new_name.split()[0] if ' ' in new_name else new_name
            
            updated_draft = draft
            
            # Replace full name first, then first name
            if old_name in updated_draft:
                updated_draft = updated_draft.replace(old_name, new_name)
                updates_made.append("story draft")
            elif old_first_name != old_name and old_first_name in updated_draft:
                updated_draft = updated_draft.replace(old_first_name, new_first_name)
                updates_made.append("story draft")
            
            if updated_draft != draft:
                self.state['draft'] = updated_draft
        
        if updates_made:
            print(f"  [OK] Updated character name in: {', '.join(updates_made)}")
        else:
            print(f"  [INFO] No other references to '{old_name}' found to update")
    
    def _propagate_location_name_change(self, old_name: str, new_name: str) -> None:
        """
        Propagate location name changes throughout the state.
        Updates all references to the old name in scene descriptions.
        
        Args:
            old_name: The old location name
            new_name: The new location name
        """
        updates_made = []
        
        # Update scenes (environmental_context references)
        if 'scenes' in self.state and self.state['scenes']:
            scenes_updated = 0
            
            for scene in self.state['scenes']:
                # Update location name in environmental_context
                if 'environmental_context' in scene and scene['environmental_context']:
                    env_context = scene['environmental_context']
                    updated_context = env_context
                    
                    # Case-insensitive replacement to handle variations
                    old_lower = old_name.lower()
                    if old_lower in updated_context.lower():
                        # Find and replace preserving original case where possible
                        import re
                        # Replace exact matches (case insensitive)
                        pattern = re.compile(re.escape(old_name), re.IGNORECASE)
                        updated_context = pattern.sub(new_name, updated_context)
                        
                        if updated_context != env_context:
                            scene['environmental_context'] = updated_context
                            scenes_updated += 1
            
            if scenes_updated > 0:
                updates_made.append(f"{scenes_updated} scene(s)")
        
        # Update draft/story text
        if 'draft' in self.state and self.state['draft']:
            draft = self.state['draft']
            
            # Case-insensitive replacement
            old_lower = old_name.lower()
            if old_lower in draft.lower():
                import re
                pattern = re.compile(re.escape(old_name), re.IGNORECASE)
                updated_draft = pattern.sub(new_name, draft)
                
                if updated_draft != draft:
                    self.state['draft'] = updated_draft
                    updates_made.append("story draft")
        
        if updates_made:
            print(f"  [OK] Updated location name in: {', '.join(updates_made)}")
        else:
            print(f"  [INFO] No other references to '{old_name}' found to update")
    
    def _update_specific_location(self, feedback: str, original_locations: list) -> None:
        """
        Update only the specific location mentioned in feedback, preserve all others.
        Uses a two-step approach:
        1. LLM identifies which location and what changes
        2. We programmatically merge the change (guarantees preservation)
        
        Args:
            feedback: User feedback about location changes
            original_locations: Current list of locations
        """
        from SagaAgent.models.locations import Location
        from pydantic import BaseModel, Field
        from typing import Optional, Literal
        
        print(f"  Analyzing which location to update...")
        
        # Start with original locations (or empty list)
        current_locations = original_locations if original_locations else []
        print(f"  Original locations count: {len(current_locations)}")
        if current_locations:
            for i, loc in enumerate(current_locations, 1):
                print(f"     {i}. {loc.get('name', 'Unknown')}")
        
        # Define a model for the LLM to identify the change
        class LocationChange(BaseModel):
            """Identifies a specific location change"""
            action: Literal["add", "modify", "remove"] = Field(description="What action to take")
            target_name: Optional[str] = Field(description="Name of location to modify/remove (if applicable)")
            new_location: Optional[Location] = Field(description="New or modified location details (if adding/modifying)")
        
        # Use LLM to identify the specific change
        llm = LLMService.create_structured_llm(
            self.state,
            LocationChange,
            creative=True
        )
        
        # Show existing locations
        existing_locations_str = ""
        if current_locations:
            for i, loc in enumerate(current_locations, 1):
                existing_locations_str += f"\n  {i}. {loc.get('name', 'Unknown')}: {loc.get('description', 'N/A')[:150]}..."
        else:
            existing_locations_str = "\n  (No existing locations)"
        
        prompt = f"""You are identifying a specific location change based on user feedback.

**User Feedback:** {feedback}

**Existing Locations:**{existing_locations_str}

**Your task:** Identify the SPECIFIC change requested:
- If adding a new location: action="add", provide new_location details
- If modifying an existing location: action="modify", provide target_name and new_location with updated details
- If removing a location: action="remove", provide target_name

**IMPORTANT:** Only identify the ONE specific change. We will preserve all other locations programmatically.

Analyze the feedback and return the specific change identified."""

        try:
            change = llm.invoke(prompt)
            
            # Now programmatically apply the change while preserving all other locations
            updated_locations = list(current_locations)  # Copy existing locations
            
            if change.action == "add":
                # Add new location
                if change.new_location:
                    new_loc = change.new_location.model_dump()
                    updated_locations.append(new_loc)
                    print(f"  [OK] Added location '{new_loc.get('name')}' (total: {len(updated_locations)})")
                    print(f"  [OK] Preserved {len(current_locations)} existing locations")
                else:
                    print(f"  [WARNING] No new location provided, keeping original")
                    
            elif change.action == "modify":
                # Modify specific location
                if change.target_name and change.new_location:
                    modified = False
                    old_name = None
                    new_name = change.new_location.name
                    
                    for i, loc in enumerate(updated_locations):
                        if loc.get('name', '').lower() == change.target_name.lower():
                            old_name = loc.get('name')
                            updated_locations[i] = change.new_location.model_dump()
                            modified = True
                            print(f"  [OK] Modified location '{change.target_name}' (total: {len(updated_locations)})")
                            print(f"  [OK] Preserved {len(updated_locations) - 1} other locations")
                            
                            # If name changed, propagate the change throughout the story
                            if old_name and old_name != new_name:
                                print(f"  [INFO] Location name changed: '{old_name}' -> '{new_name}'")
                                self._propagate_location_name_change(old_name, new_name)
                            break
                    if not modified:
                        print(f"  [WARNING] Location '{change.target_name}' not found, keeping original")
                else:
                    print(f"  [WARNING] Incomplete modification details, keeping original")
                    
            elif change.action == "remove":
                # Remove specific location
                if change.target_name:
                    removed = False
                    for i, loc in enumerate(updated_locations):
                        if loc.get('name', '').lower() == change.target_name.lower():
                            removed_name = updated_locations.pop(i).get('name')
                            removed = True
                            print(f"  [OK] Removed location '{removed_name}' (total: {len(updated_locations)})")
                            print(f"  [OK] Preserved {len(updated_locations)} other locations")
                            break
                    if not removed:
                        print(f"  [WARNING] Location '{change.target_name}' not found, keeping original")
                else:
                    print(f"  [WARNING] No target specified for removal, keeping original")
            
            # Update state with the surgically modified locations
            print(f"  Final locations count: {len(updated_locations)}")
            if updated_locations:
                for i, loc in enumerate(updated_locations, 1):
                    print(f"     {i}. {loc.get('name', 'Unknown')}")
            self.state['locations'] = updated_locations
                
        except Exception as e:
            print(f"  [ERROR] Error in surgical location update: {e}")
            import traceback
            traceback.print_exc()
            print(f"  Keeping original locations")
            self.state['locations'] = current_locations
    
    def _update_specific_character(self, feedback: str, original_characters: list) -> None:
        """
        Update only the specific character mentioned in feedback, preserve all others.
        Uses a two-step approach for guaranteed preservation.
        
        Args:
            feedback: User feedback about character changes
            original_characters: Current list of characters
        """
        from SagaAgent.models.characters import Character
        from pydantic import BaseModel, Field
        from typing import Optional, Literal
        
        print(f"  Analyzing which character to update...")
        
        # Start with original characters (or empty list)
        current_characters = original_characters if original_characters else []
        
        # Define a model for the LLM to identify the change
        class CharacterChange(BaseModel):
            """Identifies a specific character change"""
            action: Literal["add", "modify", "remove"] = Field(description="What action to take")
            target_name: Optional[str] = Field(description="Name of character to modify/remove (if applicable)")
            new_character: Optional[Character] = Field(description="New or modified character details (if adding/modifying)")
        
        # Use LLM to identify the specific change
        llm = LLMService.create_structured_llm(
            self.state,
            CharacterChange,
            creative=True
        )
        
        # Show existing characters
        existing_characters_str = ""
        if current_characters:
            for i, char in enumerate(current_characters, 1):
                existing_characters_str += f"\n  {i}. {char.get('name', 'Unknown')} ({char.get('persona_type', 'N/A')}): {char.get('appearance', 'N/A')[:100]}..."
        else:
            existing_characters_str = "\n  (No existing characters)"
        
        prompt = f"""You are identifying a specific character change based on user feedback.

**User Feedback:** {feedback}

**Existing Characters:**{existing_characters_str}

**Draft Context:** {self.state.get('draft', 'N/A')[:500]}...

**Your task:** Identify the SPECIFIC change requested:
- If adding a new character: action="add", provide new_character details
- If modifying an existing character: action="modify", provide target_name and new_character with updated details
- If removing a character: action="remove", provide target_name

**IMPORTANT:** Only identify the ONE specific change. We will preserve all other characters programmatically.

Analyze the feedback and return the specific change identified."""

        try:
            change = llm.invoke(prompt)
            
            # Now programmatically apply the change while preserving all other characters
            updated_characters = list(current_characters)  # Copy existing characters
            
            if change.action == "add":
                # Add new character
                if change.new_character:
                    new_char = change.new_character.model_dump()
                    updated_characters.append(new_char)
                    print(f"  [OK] Added character '{new_char.get('name')}' (total: {len(updated_characters)})")
                    print(f"  [OK] Preserved {len(current_characters)} existing characters")
                else:
                    print(f"  [WARNING] No new character provided, keeping original")
                    
            elif change.action == "modify":
                # Modify specific character
                if change.target_name and change.new_character:
                    modified = False
                    old_name = None
                    new_name = change.new_character.name
                    
                    for i, char in enumerate(updated_characters):
                        if char.get('name', '').lower() == change.target_name.lower():
                            old_name = char.get('name')
                            updated_characters[i] = change.new_character.model_dump()
                            modified = True
                            print(f"  [OK] Modified character '{change.target_name}' (total: {len(updated_characters)})")
                            print(f"  [OK] Preserved {len(updated_characters) - 1} other characters")
                            
                            # If name changed, propagate the change throughout the story
                            if old_name and old_name != new_name:
                                print(f"  [INFO] Character name changed: '{old_name}' -> '{new_name}'")
                                self._propagate_character_name_change(old_name, new_name)
                            break
                    if not modified:
                        print(f"  [WARNING] Character '{change.target_name}' not found, keeping original")
                else:
                    print(f"  [WARNING] Incomplete modification details, keeping original")
                    
            elif change.action == "remove":
                # Remove specific character
                if change.target_name:
                    removed = False
                    for i, char in enumerate(updated_characters):
                        if char.get('name', '').lower() == change.target_name.lower():
                            removed_name = updated_characters.pop(i).get('name')
                            removed = True
                            print(f"  [OK] Removed character '{removed_name}' (total: {len(updated_characters)})")
                            print(f"  [OK] Preserved {len(updated_characters)} other characters")
                            break
                    if not removed:
                        print(f"  [WARNING] Character '{change.target_name}' not found, keeping original")
                else:
                    print(f"  [WARNING] No target specified for removal, keeping original")
            
            # Update state with the surgically modified characters
            self.state['characters'] = updated_characters
                
        except Exception as e:
            print(f"  [ERROR] Error in surgical character update: {e}")
            import traceback
            traceback.print_exc()
            print(f"  Keeping original characters")
            self.state['characters'] = current_characters
    
    def _update_specific_dialogue(self, feedback: str, original_dialogue_scenes: list) -> None:
        """
        Update only the specific dialogue mentioned in feedback, preserve all others.
        Uses a two-step approach for guaranteed preservation.
        
        Args:
            feedback: User feedback about dialogue changes
            original_dialogue_scenes: Current list of dialogue scenes
        """
        from SagaAgent.models.dialogue import Dialogue
        from pydantic import BaseModel, Field
        from typing import Optional, Literal
        
        print(f"  Analyzing which dialogue to update...")
        
        # Start with original dialogue scenes (or empty list)
        current_dialogue = original_dialogue_scenes if original_dialogue_scenes else []
        
        # Define a model for the LLM to identify the change
        class DialogueIdentification(BaseModel):
            """Identifies a specific dialogue line by index or character"""
            target_index: Optional[int] = Field(description="Index (1-based) of dialogue line to modify/remove")
            target_character: Optional[str] = Field(description="Character name whose dialogue to modify")
        
        class DialogueChange(BaseModel):
            """Identifies a specific dialogue change"""
            action: Literal["add", "modify", "remove"] = Field(description="What action to take")
            identification: Optional[DialogueIdentification] = Field(description="How to identify the target line")
            new_dialogue: Optional[Dialogue] = Field(description="New dialogue (if adding)")
            modified_line: Optional[str] = Field(description="Modified dialogue text (if modifying)")
            scene_number: Optional[int] = Field(description="Scene number for new/modified dialogue")
        
        # Use LLM to identify the specific change
        llm = LLMService.create_structured_llm(
            self.state,
            DialogueChange,
            creative=True
        )
        
        # Show existing dialogue
        existing_dialogue_str = ""
        if current_dialogue:
            for i, dlg in enumerate(current_dialogue, 1):
                char_name = dlg.get('character_name', 'UNKNOWN')
                scene_num = dlg.get('scene_number', 0)
                line = dlg.get('line', '')[:80]
                existing_dialogue_str += f"\n  {i}. {char_name} (Scene {scene_num}): \"{line}...\""
        else:
            existing_dialogue_str = "\n  (No existing dialogue)"
        
        # Get character names for context
        character_names = [char.get('name', 'Unknown') for char in self.state.get('characters', [])]
        
        prompt = f"""You are identifying a specific dialogue change based on user feedback.

**User Feedback:** {feedback}

**Existing Dialogue:**{existing_dialogue_str}

**Characters:** {', '.join(character_names) if character_names else 'None'}

**Your task:** Identify the SPECIFIC change requested:
- If adding new dialogue: action="add", provide new_dialogue (character_name + line) and scene_number
- If modifying existing: action="modify", provide identification (index or character) and modified_line
- If removing: action="remove", provide identification (index or character)

**IMPORTANT:** Only identify the ONE specific change. We will preserve all other dialogue programmatically.

Analyze the feedback and return the specific change identified."""

        try:
            change = llm.invoke(prompt)
            
            # Now programmatically apply the change while preserving all other dialogue
            updated_dialogue = list(current_dialogue)  # Copy existing dialogue
            
            if change.action == "add":
                # Add new dialogue line
                if change.new_dialogue:
                    new_line = {
                        'character_name': change.new_dialogue.character_name,
                        'scene_number': change.scene_number or len(updated_dialogue) + 1,
                        'line': change.new_dialogue.line
                    }
                    updated_dialogue.append(new_line)
                    print(f"  [OK] Added dialogue for '{new_line['character_name']}' (total: {len(updated_dialogue)})")
                    print(f"  [OK] Preserved {len(current_dialogue)} existing lines")
                else:
                    print(f"  [WARNING] No new dialogue provided, keeping original")
                    
            elif change.action == "modify":
                # Modify specific dialogue line
                if change.identification and change.modified_line:
                    modified = False
                    if change.identification.target_index:
                        idx = change.identification.target_index - 1  # Convert to 0-based
                        if 0 <= idx < len(updated_dialogue):
                            updated_dialogue[idx]['line'] = change.modified_line
                            modified = True
                            print(f"  [OK] Modified dialogue line {idx + 1} (total: {len(updated_dialogue)})")
                            print(f"  [OK] Preserved {len(updated_dialogue) - 1} other lines")
                    elif change.identification.target_character:
                        for i, dlg in enumerate(updated_dialogue):
                            if dlg.get('character_name', '').lower() == change.identification.target_character.lower():
                                updated_dialogue[i]['line'] = change.modified_line
                                modified = True
                                print(f"  [OK] Modified '{change.identification.target_character}' dialogue (total: {len(updated_dialogue)})")
                                print(f"  [OK] Preserved {len(updated_dialogue) - 1} other lines")
                                break
                    if not modified:
                        print(f"  [WARNING] Target dialogue not found, keeping original")
                else:
                    print(f"  [WARNING] Incomplete modification details, keeping original")
                    
            elif change.action == "remove":
                # Remove specific dialogue line
                if change.identification:
                    removed = False
                    if change.identification.target_index:
                        idx = change.identification.target_index - 1  # Convert to 0-based
                        if 0 <= idx < len(updated_dialogue):
                            removed_char = updated_dialogue.pop(idx).get('character_name')
                            removed = True
                            print(f"  [OK] Removed dialogue line {idx + 1} (total: {len(updated_dialogue)})")
                            print(f"  [OK] Preserved {len(updated_dialogue)} other lines")
                    elif change.identification.target_character:
                        for i, dlg in enumerate(updated_dialogue):
                            if dlg.get('character_name', '').lower() == change.identification.target_character.lower():
                                removed_char = updated_dialogue.pop(i).get('character_name')
                                removed = True
                                print(f"  [OK] Removed '{removed_char}' dialogue (total: {len(updated_dialogue)})")
                                print(f"  [OK] Preserved {len(updated_dialogue)} other lines")
                                break
                    if not removed:
                        print(f"  [WARNING] Target dialogue not found, keeping original")
                else:
                    print(f"  [WARNING] No target specified for removal, keeping original")
            
            # Update state with the surgically modified dialogue
            self.state['dialogue_scenes'] = updated_dialogue
                
        except Exception as e:
            print(f"  [ERROR] Error in surgical dialogue update: {e}")
            import traceback
            traceback.print_exc()
            print(f"  Keeping original dialogue")
            self.state['dialogue_scenes'] = current_dialogue
    
    def _update_specific_scene(self, feedback: str, original_scenes: list) -> None:
        """
        Update only the specific scene mentioned in feedback, preserve all others.
        Uses a two-step approach for guaranteed preservation.
        
        Args:
            feedback: User feedback about scene changes
            original_scenes: Current list of scenes
        """
        from SagaAgent.models.scenes import Scene
        from pydantic import BaseModel, Field
        from typing import Optional, Literal
        
        print(f"  Analyzing which scene to update...")
        
        # Start with original scenes (or empty list)
        current_scenes = original_scenes if original_scenes else []
        
        # Define a model for the LLM to identify the change
        class SceneChange(BaseModel):
            """Identifies a specific scene change"""
            action: Literal["add", "modify", "remove", "insert_between"] = Field(description="What action to take: 'add' appends to end, 'insert_between' inserts and renumbers")
            target_scene_number: Optional[int] = Field(description="Scene number to modify/remove (if applicable)")
            insert_after_scene: Optional[int] = Field(description="For 'insert_between': insert after this scene number (e.g., 1 to insert between scenes 1 and 2)")
            num_scenes_to_insert: Optional[int] = Field(default=1, description="For 'insert_between': how many new scenes to insert (default: 1)")
            new_scenes: Optional[list[Scene]] = Field(description="New scene(s) to insert (for 'insert_between' when adding multiple)")
            new_scene: Optional[Scene] = Field(description="New or modified scene details (for single add/modify operations)")
        
        # Use LLM to identify the specific change
        llm = LLMService.create_structured_llm(
            self.state,
            SceneChange,
            creative=True
        )
        
        # Show existing scenes
        existing_scenes_str = ""
        if current_scenes:
            for scene in current_scenes:
                scene_num = scene.get('scene_number', 0)
                env = scene.get('environmental_context', 'N/A')[:80]
                subj = scene.get('subject_action', 'N/A')[:80]
                existing_scenes_str += f"\n  Scene {scene_num}: {env}... / {subj}..."
        else:
            existing_scenes_str = "\n  (No existing scenes)"
        
        # Check current scene count
        current_scene_count = len(current_scenes)
        
        prompt = f"""You are identifying a specific scene change based on user feedback.

**User Feedback:** {feedback}

**Current Scene Count:** {current_scene_count} scenes total

**Existing Scenes:**{existing_scenes_str}

**Draft:** {self.state.get('draft', 'N/A')[:400]}...
**Characters:** {', '.join([c.get('name', 'Unknown') for c in self.state.get('characters', [])])}
**Locations:** {', '.join([l.get('name', 'Unknown') for l in self.state.get('locations', [])])}

**Your task:** Identify the SPECIFIC change requested:

- **Adding at the end**: action="add", provide new_scene with all details
- **Inserting between existing scenes**: action="insert_between", provide:
  * insert_after_scene: scene number to insert after (e.g., 1 to insert between scenes 1 and 2)
  * num_scenes_to_insert: how many new scenes to add (count them from feedback)
  * new_scenes: list of new scene objects with temporary scene numbers
  * Example: "add 2 scenes between scene 1 and 2" → insert_after_scene=1, num_scenes_to_insert=2
- **Modifying existing scene**: action="modify", provide target_scene_number and new_scene with updated details
- **Removing a scene**: action="remove", provide target_scene_number

**CRITICAL SCENE COUNT RULE (HIGHEST PRIORITY):**
- The original user_view file has EXACTLY {current_scene_count} scenes
- You MUST maintain this exact count UNLESS feedback contains explicit keywords: "add scene", "insert scene", "more scenes", etc.
- If feedback says "improve scene X", "make scene Y better", "change scene Z" → use action="modify" (preserves count)
- If feedback says "add scene", "insert scene between X and Y", "need more scenes" → use action="add" or "insert_between" (increases count)
- When in doubt: DEFAULT TO "modify" to preserve the scene count from the original user_view file
- The scene count from the loaded user_view file is SACRED and should only change with explicit user authorization

**IMPORTANT NOTES:**
- "Between scene X and Y" means insert_after_scene=X (the new scene(s) will go after X, before Y)
- For insert_between, we'll automatically renumber all scenes after the insertion point
- For insert_between with multiple scenes, provide them in new_scenes list (not new_scene)
- Only identify the ONE specific change. We will handle renumbering programmatically.

Analyze the feedback and return the specific change identified."""

        try:
            change = llm.invoke(prompt)
            
            # Now programmatically apply the change while preserving all other scenes
            updated_scenes = list(current_scenes)  # Copy existing scenes
            
            if change.action == "add":
                # Add new scene at the end
                if change.new_scene:
                    new_scene = change.new_scene.model_dump()
                    updated_scenes.append(new_scene)
                    print(f"  [OK] Added scene {new_scene.get('scene_number')} (total: {len(updated_scenes)})")
                    print(f"  [OK] Preserved {len(current_scenes)} existing scenes")
                else:
                    print(f"  [WARNING] No new scene provided, keeping original")
            
            elif change.action == "insert_between":
                # Insert scene(s) between existing scenes and renumber
                if change.insert_after_scene is not None:
                    insert_after = change.insert_after_scene
                    num_to_insert = change.num_scenes_to_insert or 1
                    
                    # Get the new scenes to insert
                    scenes_to_insert = []
                    if change.new_scenes and len(change.new_scenes) > 0:
                        scenes_to_insert = [s.model_dump() for s in change.new_scenes]
                    elif change.new_scene:
                        scenes_to_insert = [change.new_scene.model_dump()]
                    
                    if not scenes_to_insert:
                        print(f"  [WARNING] No new scenes provided for insertion, keeping original")
                    else:
                        # Find the insertion point
                        insert_index = None
                        for i, scene in enumerate(updated_scenes):
                            if scene.get('scene_number') == insert_after:
                                insert_index = i + 1
                                break
                        
                        if insert_index is None:
                            print(f"  [WARNING] Scene {insert_after} not found, appending to end")
                            insert_index = len(updated_scenes)
                        
                        # Assign proper scene numbers to new scenes
                        for i, new_scene in enumerate(scenes_to_insert):
                            new_scene['scene_number'] = insert_after + 1 + i
                        
                        # Renumber all scenes after the insertion point
                        for scene in updated_scenes[insert_index:]:
                            scene['scene_number'] = scene.get('scene_number', 0) + len(scenes_to_insert)
                        
                        # Insert the new scenes
                        for i, new_scene in enumerate(scenes_to_insert):
                            updated_scenes.insert(insert_index + i, new_scene)
                        
                        print(f"  [OK] Total scenes: {len(updated_scenes)}")
                        
                        # Show the new scene numbering
                        scene_nums = [s.get('scene_number') for s in updated_scenes]
                        print(f"  [OK] Scene numbers now: {scene_nums}")
                else:
                    print(f"  [WARNING] No insertion point specified, keeping original")
                    
            elif change.action == "modify":
                # Modify specific scene
                if change.target_scene_number and change.new_scene:
                    modified = False
                    for i, scene in enumerate(updated_scenes):
                        if scene.get('scene_number') == change.target_scene_number:
                            updated_scenes[i] = change.new_scene.model_dump()
                            modified = True
                            print(f"  [OK] Modified scene {change.target_scene_number} (total: {len(updated_scenes)})")
                            print(f"  [OK] Preserved {len(updated_scenes) - 1} other scenes")
                            break
                    if not modified:
                        print(f"  [WARNING] Scene {change.target_scene_number} not found, keeping original")
                else:
                    print(f"  [WARNING] Incomplete modification details, keeping original")
                    
            elif change.action == "remove":
                # Remove specific scene
                if change.target_scene_number:
                    removed = False
                    for i, scene in enumerate(updated_scenes):
                        if scene.get('scene_number') == change.target_scene_number:
                            removed_num = updated_scenes.pop(i).get('scene_number')
                            removed = True
                            print(f"  [OK] Removed scene {removed_num} (total: {len(updated_scenes)})")
                            print(f"  [OK] Preserved {len(updated_scenes)} other scenes")
                            break
                    if not removed:
                        print(f"  [WARNING] Scene {change.target_scene_number} not found, keeping original")
                else:
                    print(f"  [WARNING] No target specified for removal, keeping original")
            
            # Update state with the surgically modified scenes
            self.state['scenes'] = updated_scenes
                
        except Exception as e:
            print(f"  [ERROR] Error in surgical scene update: {e}")
            import traceback
            traceback.print_exc()
            print(f"  Keeping original scenes")
            self.state['scenes'] = current_scenes
    
    def update_component(
        self, 
        component_name: str, 
        feedback: str
    ) -> dict:
        """
        Update a specific component based on feedback.
        
        Args:
            component_name: Name of the component to update
            feedback: Specific feedback for the update
            
        Returns:
            Updated state after component update
        """
        print(f"\n{'='*70}")
        print(f"UPDATING COMPONENT: {component_name.upper()}")
        print(f"{'='*70}")
        print(f"Feedback: {feedback[:150]}...")
        print()
        
        # Map component names to feedback keys and node functions
        component_map = {
            'draft': ('draft_feedback', create_initial_draft),
            'characters': ('characters_feedback', create_characters),
            'dialogue': ('dialogue_feedback', create_dialogue),
            'locations': ('locations_feedback', create_locations),
            'visual_lookbook': ('visual_lookbook_feedback', define_visual_language),
            'scenes': ('scenes_feedback', create_scenes)
        }
        
        if component_name not in component_map:
            print(f"[WARNING] Unknown component: {component_name}")
            return self.state
        
        feedback_key, node_function = component_map[component_name]
        
        # IMPORTANT: Preserve ALL components that are not being updated
        # This ensures that only the explicitly requested component changes
        # NOTE: We ALWAYS get the original values, even for the target component,
        # because surgical updates need the original list to preserve unchanged items!
        original_title = self.state.get('title')
        original_genre = self.state.get('genre')
        original_tone = self.state.get('tone')
        original_visual_lookbook = self.state.get('visual_lookbook')
        original_draft = self.state.get('draft')
        original_characters = self.state.get('characters')
        original_locations = self.state.get('locations')
        original_dialogue_scenes = self.state.get('dialogue_scenes')
        original_scenes = self.state.get('scenes')
        
        # Add feedback to state
        self.state[feedback_key] = feedback
        
        # Special handling for draft - only update the draft text, nothing else
        if component_name == 'draft':
            print(f"  Updating draft text only (preserving all other components)...")
            try:
                # Call the draft node to get updated draft
                result = node_function(self.state)
                
                # ONLY update the draft field, ignore everything else the node might return
                if 'draft' in result:
                    self.state['draft'] = result['draft']
                    print(f"  [OK] Draft updated successfully")
                    print(f"  [OK] All other components preserved (characters, locations, dialogue, scenes, etc.)")
                else:
                    print(f"  [WARNING] No draft returned, keeping original")
                
            except Exception as e:
                print(f"  [ERROR] Error updating draft: {e}")
                import traceback
                traceback.print_exc()
            
            # Clear feedback and return early
            if feedback_key in self.state:
                del self.state[feedback_key]
            print(f"{'='*70}\n")
            return self.state
        
        # Special handling for locations - only update the specific location mentioned
        if component_name == 'locations':
            self._update_specific_location(feedback, original_locations)
            preserved_attrs = ["title", "genre", "tone", "draft", "characters", "dialogue", "visual_lookbook", "scenes"]
            print(f"[OK] locations updated surgically (specific location only)")
            print(f"  Preserved: {', '.join(preserved_attrs)}")
            
            # Clear feedback and return early
            if feedback_key in self.state:
                del self.state[feedback_key]
            print(f"{'='*70}\n")
            return self.state
        
        # Special handling for characters - only update the specific character mentioned
        if component_name == 'characters':
            self._update_specific_character(feedback, original_characters)
            preserved_attrs = ["title", "genre", "tone", "draft", "locations", "dialogue", "visual_lookbook", "scenes"]
            print(f"[OK] characters updated surgically (specific character only)")
            print(f"  Preserved: {', '.join(preserved_attrs)}")
            
            # Clear feedback and return early
            if feedback_key in self.state:
                del self.state[feedback_key]
            print(f"{'='*70}\n")
            return self.state
        
        # Special handling for dialogue - only update the specific dialogue line mentioned
        if component_name == 'dialogue':
            self._update_specific_dialogue(feedback, original_dialogue_scenes)
            preserved_attrs = ["title", "genre", "tone", "draft", "characters", "locations", "visual_lookbook", "scenes"]
            print(f"[OK] dialogue updated surgically (specific dialogue only)")
            print(f"  Preserved: {', '.join(preserved_attrs)}")
            
            # Clear feedback and return early
            if feedback_key in self.state:
                del self.state[feedback_key]
            print(f"{'='*70}\n")
            return self.state
        
        # Special handling for scenes - only update the specific scene mentioned
        if component_name == 'scenes':
            # Get the preserved scene count from the loaded user_view file
            original_scene_count = self.state.get('number_of_scenes', 12)
            current_scene_count = len(original_scenes) if original_scenes else original_scene_count
            
            print(f"  [INFO] Original user_view had {current_scene_count} scenes")
            
            # Check if user feedback explicitly requests adding more scenes
            # ONLY these keywords allow scene count to increase from the original
            feedback_lower = feedback.lower()
            increase_keywords = ['add scene', 'add more scene', 'need more scene', 'create more scene', 
                                'insert scene', 'additional scene', 'more scenes', 'expand scenes',
                                'increase scene count', 'add another scene', 'add new scene']
            
            allow_increase = any(keyword in feedback_lower for keyword in increase_keywords)
            
            if allow_increase:
                print(f"  [AUTHORIZED] User explicitly requested 'add scene' - allowing scene count increase from {current_scene_count}")
                self.state['allow_scene_increase'] = True
            else:
                print(f"  [ENFORCED] Scene count will be preserved from original user_view file")
                self.state['allow_scene_increase'] = False
            
            # Ensure number_of_scenes is set to the original count for enforcement
            self.state['number_of_scenes'] = current_scene_count
            
            self._update_specific_scene(feedback, original_scenes)
            preserved_attrs = ["title", "genre", "tone", "draft", "characters", "locations", "dialogue", "visual_lookbook"]
            
            # Clear feedback and flags after update
            if feedback_key in self.state:
                del self.state[feedback_key]
            if 'allow_scene_increase' in self.state:
                del self.state['allow_scene_increase']  # Clean up flag after use
            print(f"{'='*70}\n")
            return self.state
        
        # Special handling for visual_lookbook - only update the lookbook, nothing else
        if component_name == 'visual_lookbook':
            print(f"  Updating visual lookbook only (preserving all other components)...")
            try:
                # Call the visual lookbook node to get updated lookbook
                result = node_function(self.state)
                
                # ONLY update the visual_lookbook field, ignore everything else
                if 'visual_lookbook' in result:
                    self.state['visual_lookbook'] = result['visual_lookbook']
                    print(f"  [OK] Visual lookbook updated successfully")
                    print(f"  [OK] All other components preserved (draft, characters, locations, dialogue, scenes, etc.)")
                else:
                    print(f"  [WARNING] No visual lookbook returned, keeping original")
                
            except Exception as e:
                print(f"  [ERROR] Error updating visual lookbook: {e}")
                import traceback
                traceback.print_exc()
            
            # Clear feedback and return early
            if feedback_key in self.state:
                del self.state[feedback_key]
            print(f"{'='*70}\n")
            return self.state
        
        # Call the appropriate node function for other components
        try:
            result = node_function(self.state)
            self.state.update(result)
            
            # Restore ALL non-target components (preserve everything except what was explicitly updated)
            preserved_attrs = []
            
            # Always preserve core attributes
            if original_title:
                self.state['title'] = original_title
                preserved_attrs.append("title")
            if original_genre:
                self.state['genre'] = original_genre
                preserved_attrs.append("genre")
            if original_tone:
                self.state['tone'] = original_tone
                preserved_attrs.append("tone")
            
            # Preserve non-target components (don't restore the component we just updated!)
            if component_name != 'draft' and original_draft is not None:
                self.state['draft'] = original_draft
                preserved_attrs.append("draft")
            if component_name != 'characters' and original_characters is not None:
                self.state['characters'] = original_characters
                preserved_attrs.append("characters")
            if component_name != 'locations' and original_locations is not None:
                self.state['locations'] = original_locations
                preserved_attrs.append("locations")
            if component_name != 'dialogue' and original_dialogue_scenes is not None:
                self.state['dialogue_scenes'] = original_dialogue_scenes
                preserved_attrs.append("dialogue")
            if original_visual_lookbook is not None:
                self.state['visual_lookbook'] = original_visual_lookbook
                preserved_attrs.append("visual_lookbook")
            if component_name != 'scenes' and original_scenes is not None:
                self.state['scenes'] = original_scenes
                preserved_attrs.append("scenes")
            
            if preserved_attrs:
                print(f"[OK] {component_name} updated successfully")
                print(f"  Preserved: {', '.join(preserved_attrs)}")
            else:
                print(f"[OK] {component_name} updated successfully")
        except Exception as e:
            print(f"[ERROR] Error updating {component_name}: {e}")
            import traceback
            traceback.print_exc()
        
        # Clear feedback after update
        if feedback_key in self.state:
            del self.state[feedback_key]
        
        print(f"{'='*70}\n")
        
        return self.state
    
    def compile_and_export(self) -> Tuple[str, str]:
        """
        Compile the final script and export user_view only.
        
        Returns:
            Tuple of (json_filepath, markdown_filepath)
        """
        print(f"\n{'='*70}")
        print(f"COMPILING AND EXPORTING")
        print(f"{'='*70}\n")
        
        # Compile final script
        print("Compiling final script...")
        compile_result = compile_script(self.state)
        self.state.update(compile_result)
        print("[OK] Script compiled")
        
        # Export user view only (skip individual component exports)
        print("\nExporting user view...")
        user_view_result = export_user_view(self.state)
        self.state.update(user_view_result)
        
        user_view_json = self.state.get('user_view_json', '')
        user_view_markdown = self.state.get('user_view_markdown', '')
        
        print(f"[OK] User view exported")
        print(f"\n{'='*70}")
        print(f"EXPORT COMPLETE")
        print(f"{'='*70}")
        print(f"JSON: {user_view_json}")
        print(f"Markdown: {user_view_markdown}")
        print(f"{'='*70}\n")
        
        return user_view_json, user_view_markdown
    
    def identify_components_with_llm(
        self, 
        user_feedback: str, 
        user_view_data: dict
    ) -> ComponentIdentification:
        """
        Use LLM to intelligently identify which components need updating.
        
        Args:
            user_feedback: User's feedback text
            user_view_data: Current story state
            
        Returns:
            ComponentIdentification with primary component, dependencies, and feedback
        """
        print(f"\n{'='*70}")
        print(f"LLM-POWERED COMPONENT IDENTIFICATION")
        print(f"{'='*70}")
        print(f"Using model: {self.state.get('model_provider', 'openai')}")
        print(f"Analyzing user intent...\n")
        
        # Create LLM with structured output
        llm = LLMService.create_structured_llm(
            self.state, 
            ComponentIdentification, 
            creative=False  # Analytical task
        )
        
        # Generate prompt
        prompt = get_component_identification_prompt(user_feedback, user_view_data)
        
        # Get LLM response
        try:
            result = llm.invoke(prompt)
            
            print(f"[OK] Analysis complete")
            print(f"\n{'='*70}")
            print(f"COMPONENT IDENTIFICATION RESULT")
            print(f"{'='*70}")
            print(f"User Intent: {result.user_intent}")
            print(f"Primary Component: {result.primary_component}")
            print(f"Dependent Components: {', '.join(result.dependent_components) if result.dependent_components else 'None'}")
            print(f"\nReasoning: {result.reasoning}")
            print(f"{'='*70}\n")
            
            return result
            
        except Exception as e:
            print(f"[ERROR] Error during LLM analysis: {e}")
            print("Falling back to keyword-based detection...")
            
            # Fallback to simple keyword matching
            feedback_lower = user_feedback.lower()
            component_keywords = {
                'characters': ['character', 'protagonist', 'person', 'people', 'cast'],
                'draft': ['draft', 'story', 'narrative', 'plot', 'storyline'],
                'dialogue': ['dialogue', 'dialog', 'conversation', 'lines', 'speech'],
                'locations': ['location', 'place', 'setting', 'scene location', 'where'],
                'visual_lookbook': ['visual', 'style', 'look', 'aesthetic', 'color', 'camera'],
                'scenes': ['scene', 'shot', 'sequence', 'scene breakdown']
            }
            
            primary = None
            for component, keywords in component_keywords.items():
                for keyword in keywords:
                    if keyword in feedback_lower:
                        primary = component
                        break
                if primary:
                    break
            
            if not primary:
                primary = 'draft'  # Default fallback
            
            # Create fallback response with NO dependencies (conservative approach)
            # User can always make additional requests if they want more components updated
            return ComponentIdentification(
                user_intent=user_feedback,
                primary_component=primary,
                dependent_components=[],  # CONSERVATIVE: No auto-dependencies in fallback
                reasoning=f"Fallback keyword detection identified '{primary}' component (updating only this component)",
                primary_feedback=user_feedback
            )
    
    def orchestrate_revision(
        self,
        user_view_filepath: str,
        user_feedback: str = "",
        auto_apply: bool = True,
        targeted_update: bool = True
    ) -> Tuple[str, str]:
        """
        Complete orchestration workflow:
        1. Load user_view file
        2. Analyze with LLM (if not targeted)
        3. Display analysis
        4. Update components based on feedback
        5. Export new user_view
        
        Args:
            user_view_filepath: Path to the user_view JSON file
            user_feedback: Optional additional feedback from the user
            auto_apply: If True (default), automatically apply all updates without confirmation.
                       If False, prompt user for confirmation before applying updates.
            targeted_update: If True (default), only update the specific component mentioned
                           in user feedback. If False, analyze all components and update what's needed.
            
        Returns:
            Tuple of (new_json_filepath, new_markdown_filepath)
        """
        print(f"\n{'#'*70}")
        print(f"# ORCHESTRATOR AGENT - STORY REVISION WORKFLOW")
        print(f"{'#'*70}\n")
        
        # Step 1: Load user_view
        user_view_data = self.load_user_view(user_view_filepath)
        
        # Step 2: Determine update strategy
        if targeted_update and user_feedback:
            # Targeted update: Use ReAct agent or direct LLM to identify components
            if self.use_react:
                # Use ReAct agent for reasoning
                print(f"\n{'='*70}")
                print(f"USING REACT AGENT FOR INTELLIGENT REASONING")
                print(f"{'='*70}\n")
                
                react_agent = ReactOrchestratorAgent(self.state, user_view_data)
                decision = react_agent.analyze_feedback(user_feedback)
                
                # Convert ReAct decision to ComponentIdentification format
                component_id = ComponentIdentification(
                    user_intent=user_feedback,
                    primary_component=decision.get('primary_component', 'draft'),
                    dependent_components=decision.get('dependent_components', []),
                    reasoning=decision.get('reasoning', 'ReAct agent decision'),
                    primary_feedback=user_feedback
                )
            else:
                # Use direct LLM (original method)
                component_id = self.identify_components_with_llm(user_feedback, user_view_data)
            
            # Build list of components to update (ONLY primary component by default)
            # We do NOT update dependent components to avoid unintended changes
            # The user should explicitly request changes to other components if needed
            components_to_update = [component_id.primary_component]
            
            # Log dependent components but don't update them
            if component_id.dependent_components:
                print(f"\n[NOTE] The following components are related to {component_id.primary_component}")
                print(f"   but will NOT be automatically updated: {', '.join(component_id.dependent_components)}")
                print(f"   If you need to update them, please provide explicit feedback for each.")
                print()
            
            # Create a simple "analysis" for compatibility with the rest of the code
            class SimpleAnalysis:
                def __init__(self, component_id, components_list, original_feedback):
                    self.story_coherence_score = None
                    self.overall_assessment = f"Targeted update: {component_id.user_intent}"
                    self.suggested_improvements = []
                    self.component_feedback = []
                    self._components_to_update = components_list
                    self._component_id = component_id
                    self._original_feedback = original_feedback
                
                def get_components_to_update(self):
                    return self._components_to_update
                
                def get_feedback_for_component(self, component_name):
                    if component_name == self._component_id.primary_component:
                        # For the primary component, use the ORIGINAL user feedback
                        # This ensures explicit requests like "add character named X" are preserved
                        return self._original_feedback
                    else:
                        # For dependent components, generate minimal update instructions
                        return f"Update {component_name} to maintain coherence with changes to {self._component_id.primary_component}. Keep changes minimal."
            
            analysis = SimpleAnalysis(component_id, components_to_update, user_feedback)
            
            print(f"\n[OK] Target components identified: {', '.join(components_to_update)}")
            print(f"{'='*70}\n")
        
        # Full analysis mode
        if not targeted_update or not user_feedback:
            print(f"{'='*70}")
            print(f"FULL ANALYSIS MODE")
            print(f"{'='*70}")
            print(f"Analyzing all components and updating what needs improvement.")
            print(f"{'='*70}\n")
        
        # Step 2: Analyze with LLM
        analysis = self.analyze_user_view(user_view_data, user_feedback)
        
        # Step 3: Display analysis
        self.display_analysis(analysis)
        
        # Step 4: Get components to update
        components_to_update = analysis.get_components_to_update()
        
        if not components_to_update:
            print("[OK] No components need updating.")
            if targeted_update:
                print("[WARNING] Could not identify a specific component to update from your feedback.")
                print("Please mention the component explicitly (e.g., 'character', 'dialogue', 'scene', etc.)")
                return "", ""
            print("\nExporting current state...")
            # Still update state and export
            self.update_state_from_user_view(user_view_data)
            return self.compile_and_export()
        
        # Step 5: Confirm updates (unless auto_apply)
        if not auto_apply:
            print(f"\n📋 Components to Update ({len(components_to_update)}):")
            for i, component in enumerate(components_to_update, 1):
                feedback = analysis.get_feedback_for_component(component)
                print(f"  {i}. {component}")
                print(f"     → {feedback[:100]}...")
            
            confirm = input("\nProceed with updates? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("[CANCELLED] Updates cancelled by user")
                return "", ""
        
        # Step 6: Update state from user_view
        self.update_state_from_user_view(user_view_data)
        
        # Step 7: Update components in order
        print(f"\n{'='*70}")
        print(f"APPLYING UPDATES")
        print(f"{'='*70}\n")
        
        for component in components_to_update:
            feedback = analysis.get_feedback_for_component(component)
            if feedback:
                self.update_component(component, feedback)
        
        # Step 8: Export
        if targeted_update:
            # In targeted mode, only export without recompiling
            # This preserves all other components exactly as they were
            print(f"\n{'='*70}")
            print(f"EXPORTING (TARGETED MODE - NO RECOMPILATION)")
            print(f"{'='*70}")
            print(f"Preserving all components except: {', '.join(components_to_update)}")
            print(f"{'='*70}\n")
            
            # Export user view only (skip individual component exports)
            print("Exporting user view...")
            user_view_result = export_user_view(self.state)
            self.state.update(user_view_result)
            
            user_view_json = self.state.get('user_view_json', '')
            user_view_markdown = self.state.get('user_view_markdown', '')
            
            print(f"\n{'='*70}")
            print(f"EXPORT COMPLETE (TARGETED UPDATE)")
            print(f"{'='*70}")
            print(f"JSON: {user_view_json}")
            print(f"Markdown: {user_view_markdown}")
            print(f"{'='*70}\n")
            
            new_json, new_markdown = user_view_json, user_view_markdown
        else:
            # Full mode: Compile and export (may affect other components)
            new_json, new_markdown = self.compile_and_export()
        
        print(f"\n{'#'*70}")
        print(f"# REVISION COMPLETE")
        print(f"{'#'*70}")
        print(f"\nNew user_view files:")
        print(f"  - JSON: {new_json}")
        print(f"  - Markdown: {new_markdown}")
        print(f"\n{'#'*70}\n")
        
        return new_json, new_markdown
    
    def interactive_revision(self, user_view_filepath: str) -> Tuple[str, str]:
        """
        Interactive revision workflow with component-by-component confirmation.
        
        Args:
            user_view_filepath: Path to the user_view JSON file
            
        Returns:
            Tuple of (new_json_filepath, new_markdown_filepath)
        """
        print(f"\n{'#'*70}")
        print(f"# ORCHESTRATOR AGENT - INTERACTIVE REVISION")
        print(f"{'#'*70}\n")
        
        # Step 1: Load user_view
        user_view_data = self.load_user_view(user_view_filepath)
        
        # Step 2: Get user feedback
        print("Optional: Provide your own feedback (or press Enter to skip):")
        user_feedback = input("> ").strip()
        
        # Step 3: Analyze with LLM
        analysis = self.analyze_user_view(user_view_data, user_feedback)
        
        # Step 4: Display analysis
        self.display_analysis(analysis)
        
        # Step 5: Get components to update
        components_to_update = analysis.get_components_to_update()
        
        if not components_to_update:
            print("[OK] No components need updating. Story is in good shape!")
            print("\nExporting current state...")
            self.update_state_from_user_view(user_view_data)
            return self.compile_and_export()
        
        # Step 6: Update state from user_view
        self.update_state_from_user_view(user_view_data)
        
        # Step 7: Component-by-component updates with confirmation
        print(f"\n{'='*70}")
        print(f"INTERACTIVE COMPONENT UPDATES")
        print(f"{'='*70}\n")
        
        for i, component in enumerate(components_to_update, 1):
            feedback = analysis.get_feedback_for_component(component)
            
            print(f"\n[{i}/{len(components_to_update)}] {component.upper()}")
            print(f"Feedback: {feedback}")
            
            choice = input(f"\nUpdate {component}? (yes/no/edit): ").strip().lower()
            
            if choice in ['yes', 'y']:
                self.update_component(component, feedback)
            elif choice in ['edit', 'e']:
                print(f"Enter custom feedback for {component}:")
                custom_feedback = input("> ").strip()
                if custom_feedback:
                    self.update_component(component, custom_feedback)
                else:
                    print(f"[SKIPPED] {component} (no feedback provided)")
            else:
                print(f"[SKIPPED] {component}")
        
        # Step 8: Compile and export
        new_json, new_markdown = self.compile_and_export()
        
        print(f"\n{'#'*70}")
        print(f"# INTERACTIVE REVISION COMPLETE")
        print(f"{'#'*70}")
        print(f"\nNew user_view files:")
        print(f"  - JSON: {new_json}")
        print(f"  - Markdown: {new_markdown}")
        print(f"\n{'#'*70}\n")
        
        return new_json, new_markdown


def main():
    """Main entry point for orchestrator agent"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m SagaAgent.orchestrator <user_view_file.json> [--auto] [--interactive]")
        print("\nOptions:")
        print("  --auto        Auto-apply all updates without confirmation")
        print("  --interactive Use interactive mode with component-by-component confirmation")
        sys.exit(1)
    
    user_view_file = sys.argv[1]
    auto_apply = '--auto' in sys.argv
    interactive = '--interactive' in sys.argv
    
    # Create orchestrator
    orchestrator = OrchestratorAgent()
    
    # Run appropriate workflow
    if interactive:
        orchestrator.interactive_revision(user_view_file)
    else:
        orchestrator.orchestrate_revision(user_view_file, auto_apply=auto_apply)


if __name__ == "__main__":
    main()

