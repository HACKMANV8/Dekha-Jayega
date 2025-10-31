"""
Orchestrator Agent for SagaAgent.

This agent analyzes existing saga narrative files, gets LLM feedback,
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
from SagaAgent.services.export_service import ExportService

# Import node functions
from SagaAgent.nodes import (
    generate_concept_node,
    generate_world_lore_node,
    generate_factions_node,
    generate_characters_node,
    generate_plot_arcs_node,
    generate_questlines_node,
)


class OrchestratorAgent:
    """
    Orchestrator agent that analyzes and revises saga narrative components.
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
    
    def load_saga_file(self, filepath: str, component_type: str = None) -> dict:
        """
        Load a saga JSON file (concept, world_lore, factions, characters, plot_arcs, or questlines).
        
        Args:
            filepath: Path to the saga JSON file
            component_type: Type of component being loaded (auto-detected from filename if None)
            
        Returns:
            The loaded saga data as a dictionary
        """
        print(f"\n{'='*70}")
        print(f"LOADING SAGA FILE")
        print(f"{'='*70}")
        print(f"File: {filepath}")
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Saga file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            saga_data = json.load(f)
        
        # Auto-detect component type from filename if not provided
        if not component_type:
            filename = os.path.basename(filepath).lower()
            if 'concept' in filename:
                component_type = 'concept'
            elif 'world_lore' in filename or 'lore' in filename:
                component_type = 'world_lore'
            elif 'faction' in filename:
                component_type = 'factions'
            elif 'character' in filename:
                component_type = 'characters'
            elif 'plot' in filename or 'arc' in filename:
                component_type = 'plot_arcs'
            elif 'quest' in filename:
                component_type = 'questlines'
        
        print(f"[OK] Loaded successfully")
        print(f"  - Component Type: {component_type or 'Unknown'}")
        
        # Display component-specific info
        if isinstance(saga_data, dict):
            if 'title' in saga_data:
                print(f"  - Title: {saga_data.get('title', 'Unknown')}")
            if 'world_name' in saga_data:
                print(f"  - World: {saga_data.get('world_name', 'Unknown')}")
        elif isinstance(saga_data, list):
            print(f"  - Count: {len(saga_data)} items")
            if saga_data and isinstance(saga_data[0], dict):
                if 'name' in saga_data[0]:
                    names = [item.get('name', 'Unknown') for item in saga_data[:3]]
                    print(f"  - Items: {', '.join(names)}...")
        
        print(f"{'='*70}\n")
        
        return saga_data
    
    def analyze_saga(
        self, 
        saga_data: dict, 
        user_feedback: str = ""
    ) -> UserViewAnalysis:
        """
        Analyze a saga narrative using LLM and get structured feedback.
        
        Args:
            saga_data: The complete saga data (with all components)
            user_feedback: Optional additional feedback from the user
            
        Returns:
            Structured analysis with component feedback
        """
        print(f"\n{'='*70}")
        print(f"ANALYZING SAGA NARRATIVE WITH LLM")
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
        prompt = get_user_view_analysis_prompt(saga_data, user_feedback)
        
        # Get analysis from LLM
        print("Invoking LLM for analysis...")
        analysis = llm.invoke(prompt)
        
        print(f"[OK] Analysis complete")
        print(f"  - Narrative Coherence Score: {analysis.narrative_coherence_score}/10")
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
        print(f"SAGA NARRATIVE ANALYSIS RESULTS")
        print(f"{'='*70}")
        print(f"\nNarrative Coherence Score: {analysis.narrative_coherence_score}/10\n")
        
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
    
    def update_state_from_saga(self, saga_data: dict) -> None:
        """
        Update internal state from saga data to prepare for component updates.
        
        Args:
            saga_data: The complete saga data
        """
        print(f"Updating state from saga data...")
        
        # Transfer all saga components to state
        if 'concept' in saga_data:
            self.state['concept'] = saga_data['concept']
            if isinstance(saga_data['concept'], dict):
                self.state['topic'] = saga_data['concept'].get('title', '')
        
        if 'world_lore' in saga_data:
            self.state['world_lore'] = saga_data['world_lore']
        
        if 'factions' in saga_data:
            self.state['factions'] = saga_data['factions']
        
        if 'characters' in saga_data:
            self.state['characters'] = saga_data['characters']
        
        if 'plot_arcs' in saga_data:
            self.state['plot_arcs'] = saga_data['plot_arcs']
        
        if 'questlines' in saga_data:
            self.state['questlines'] = saga_data['questlines']
        
        print(f"[OK] State updated successfully")
    
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
            'concept': ('concept_feedback', generate_concept_node),
            'world_lore': ('world_lore_feedback', generate_world_lore_node),
            'factions': ('factions_feedback', generate_factions_node),
            'characters': ('characters_feedback', generate_characters_node),
            'plot_arcs': ('plot_arcs_feedback', generate_plot_arcs_node),
            'questlines': ('questlines_feedback', generate_questlines_node)
        }
        
        if component_name not in component_map:
            print(f"[WARNING] Unknown component: {component_name}")
            return self.state
        
        feedback_key, node_function = component_map[component_name]
        
        # Preserve ALL components that are not being updated
        original_concept = self.state.get('concept')
        original_world_lore = self.state.get('world_lore')
        original_factions = self.state.get('factions')
        original_characters = self.state.get('characters')
        original_plot_arcs = self.state.get('plot_arcs')
        original_questlines = self.state.get('questlines')
        
        # Add feedback to state
        self.state[feedback_key] = feedback
        
        # Call the appropriate node function
        try:
            result = node_function(self.state)
            self.state.update(result)
            
            # Restore ALL non-target components (preserve everything except what was explicitly updated)
            preserved_attrs = []
            
            # Preserve non-target components (don't restore the component we just updated!)
            if component_name != 'concept' and original_concept is not None:
                self.state['concept'] = original_concept
                preserved_attrs.append("concept")
            if component_name != 'world_lore' and original_world_lore is not None:
                self.state['world_lore'] = original_world_lore
                preserved_attrs.append("world_lore")
            if component_name != 'factions' and original_factions is not None:
                self.state['factions'] = original_factions
                preserved_attrs.append("factions")
            if component_name != 'characters' and original_characters is not None:
                self.state['characters'] = original_characters
                preserved_attrs.append("characters")
            if component_name != 'plot_arcs' and original_plot_arcs is not None:
                self.state['plot_arcs'] = original_plot_arcs
                preserved_attrs.append("plot_arcs")
            if component_name != 'questlines' and original_questlines is not None:
                self.state['questlines'] = original_questlines
                preserved_attrs.append("questlines")
            
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
    
    def export_saga(self) -> Tuple[List[str], List[str]]:
        """
        Export the updated saga narrative to JSON and Markdown files.
        
        Returns:
            Tuple of (json_files, markdown_files)
        """
        print(f"\n{'='*70}")
        print(f"EXPORTING SAGA NARRATIVE")
        print(f"{'='*70}\n")
        
        # Export to JSON
        print("Exporting to JSON...")
        json_result = ExportService.export_all_json(self.state)
        self.state.update(json_result)
        json_files = json_result.get('json_files', [])
        
        # Export to Markdown
        print("Exporting to Markdown...")
        md_result = ExportService.export_all_markdown(self.state)
        self.state.update(md_result)
        markdown_files = md_result.get('markdown_files', [])
        
        print(f"[OK] Saga exported")
        print(f"\n{'='*70}")
        print(f"EXPORT COMPLETE")
        print(f"{'='*70}")
        print(f"JSON Files ({len(json_files)}):")
        for f in json_files:
            print(f"  - {f}")
        print(f"\nMarkdown Files ({len(markdown_files)}):")
        for f in markdown_files:
            print(f"  - {f}")
        print(f"{'='*70}\n")
        
        return json_files, markdown_files
    
    def identify_components_with_llm(
        self, 
        user_feedback: str, 
        saga_data: dict
    ) -> ComponentIdentification:
        """
        Use LLM to intelligently identify which components need updating.
        
        Args:
            user_feedback: User's feedback text
            saga_data: Current saga state
            
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
        prompt = get_component_identification_prompt(user_feedback, saga_data)
        
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
                'concept': ['concept', 'game', 'core loop', 'mechanics', 'usp', 'genre'],
                'world_lore': ['world', 'lore', 'history', 'culture', 'setting', 'theme'],
                'factions': ['faction', 'group', 'organization', 'guild', 'clan'],
                'characters': ['character', 'person', 'protagonist', 'npc', 'hero'],
                'plot_arcs': ['plot', 'arc', 'story', 'narrative', 'campaign'],
                'questlines': ['quest', 'mission', 'task', 'objective']
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
                primary = 'concept'  # Default fallback
            
            # Create fallback response with NO dependencies (conservative approach)
            return ComponentIdentification(
                user_intent=user_feedback,
                primary_component=primary,
                dependent_components=[],  # CONSERVATIVE: No auto-dependencies in fallback
                reasoning=f"Fallback keyword detection identified '{primary}' component (updating only this component)",
                primary_feedback=user_feedback
            )
    
    def orchestrate_revision(
        self,
        saga_filepath: str,
        user_feedback: str = "",
        auto_apply: bool = True,
        targeted_update: bool = True
    ) -> Tuple[List[str], List[str]]:
        """
        Complete orchestration workflow:
        1. Load saga file(s)
        2. Analyze with LLM (if not targeted)
        3. Display analysis
        4. Update components based on feedback
        5. Export new saga files
        
        Args:
            saga_filepath: Path to a saga JSON file or directory containing saga files
            user_feedback: Optional additional feedback from the user
            auto_apply: If True (default), automatically apply all updates without confirmation.
                       If False, prompt user for confirmation before applying updates.
            targeted_update: If True (default), only update the specific component mentioned
                           in user feedback. If False, analyze all components and update what's needed.
            
        Returns:
            Tuple of (json_files, markdown_files)
        """
        print(f"\n{'#'*70}")
        print(f"# ORCHESTRATOR AGENT - SAGA REVISION WORKFLOW")
        print(f"{'#'*70}\n")
        
        # Step 1: Load saga data
        # If a directory is provided, load all saga components
        if os.path.isdir(saga_filepath):
            print(f"Loading saga from directory: {saga_filepath}")
            saga_data = self._load_saga_directory(saga_filepath)
        else:
            # Single file - load it and combine with existing state if needed
            component_data = self.load_saga_file(saga_filepath)
            # Try to build complete saga data from available files
            saga_data = self._build_complete_saga(saga_filepath, component_data)
        
        # Step 2: Determine update strategy
        if targeted_update and user_feedback:
            # Targeted update: Use LLM to identify components
            component_id = self.identify_components_with_llm(user_feedback, saga_data)
            
            # Build list of components to update (ONLY primary component by default)
            components_to_update = [component_id.primary_component]
            
            # Log dependent components but don't update them
            if component_id.dependent_components:
                print(f"\n[NOTE] The following components are related to {component_id.primary_component}")
                print(f"   but will NOT be automatically updated: {', '.join(component_id.dependent_components)}")
                print(f"   If you need to update them, please provide explicit feedback for each.")
                print()
            
            # Create a simple "analysis" for compatibility
            class SimpleAnalysis:
                def __init__(self, component_id, components_list, original_feedback):
                    self.narrative_coherence_score = None
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
                        return self._original_feedback
                    else:
                        return f"Update {component_name} to maintain coherence with changes to {self._component_id.primary_component}. Keep changes minimal."
            
            analysis = SimpleAnalysis(component_id, components_to_update, user_feedback)
            
            print(f"\n[OK] Target components identified: {', '.join(components_to_update)}")
            print(f"{'='*70}\n")
        else:
            # Full analysis mode
            print(f"{'='*70}")
            print(f"FULL ANALYSIS MODE")
            print(f"{'='*70}")
            print(f"Analyzing all components and updating what needs improvement.")
            print(f"{'='*70}\n")
            
            # Step 2: Analyze with LLM
            analysis = self.analyze_saga(saga_data, user_feedback)
            
            # Step 3: Display analysis
            self.display_analysis(analysis)
            
            # Step 4: Get components to update
            components_to_update = analysis.get_components_to_update()
            
            if not components_to_update:
                print("[OK] No components need updating.")
                if targeted_update:
                    print("[WARNING] Could not identify a specific component to update from your feedback.")
                    print("Please mention the component explicitly (e.g., 'character', 'faction', 'quest', etc.)")
                    return [], []
                print("\nExporting current state...")
                self.update_state_from_saga(saga_data)
                return self.export_saga()
        
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
                return [], []
        
        # Step 6: Update state from saga data
        self.update_state_from_saga(saga_data)
        
        # Step 7: Update components in order
        print(f"\n{'='*70}")
        print(f"APPLYING UPDATES")
        print(f"{'='*70}\n")
        
        for component in components_to_update:
            feedback = analysis.get_feedback_for_component(component)
            if feedback:
                self.update_component(component, feedback)
        
        # Step 8: Export
        json_files, markdown_files = self.export_saga()
        
        print(f"\n{'#'*70}")
        print(f"# REVISION COMPLETE")
        print(f"{'#'*70}")
        print(f"\nNew saga files:")
        print(f"  - JSON: {len(json_files)} files")
        print(f"  - Markdown: {len(markdown_files)} files")
        print(f"\n{'#'*70}\n")
        
        return json_files, markdown_files
    
    def _load_saga_directory(self, directory: str) -> dict:
        """Load all saga components from a directory"""
        saga_data = {}
        
        # Look for component files
        for filename in os.listdir(directory):
            if not filename.endswith('.json'):
                continue
            
            filepath = os.path.join(directory, filename)
            filename_lower = filename.lower()
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Determine component type from filename
                if 'concept' in filename_lower:
                    saga_data['concept'] = data
                elif 'world_lore' in filename_lower or 'lore' in filename_lower:
                    saga_data['world_lore'] = data
                elif 'faction' in filename_lower:
                    saga_data['factions'] = data
                elif 'character' in filename_lower:
                    saga_data['characters'] = data
                elif 'plot' in filename_lower or 'arc' in filename_lower:
                    saga_data['plot_arcs'] = data
                elif 'quest' in filename_lower:
                    saga_data['questlines'] = data
            except Exception as e:
                print(f"[WARNING] Could not load {filename}: {e}")
        
        return saga_data
    
    def _build_complete_saga(self, filepath: str, component_data: dict) -> dict:
        """Try to build a complete saga from a single file and related files in the same directory"""
        saga_data = {}
        
        # Get directory and look for related files
        directory = os.path.dirname(filepath)
        if directory:
            saga_data = self._load_saga_directory(directory)
        
        # Merge in the specific component data
        filename = os.path.basename(filepath).lower()
        if 'concept' in filename:
            saga_data['concept'] = component_data
        elif 'world_lore' in filename or 'lore' in filename:
            saga_data['world_lore'] = component_data
        elif 'faction' in filename:
            saga_data['factions'] = component_data
        elif 'character' in filename:
            saga_data['characters'] = component_data
        elif 'plot' in filename or 'arc' in filename:
            saga_data['plot_arcs'] = component_data
        elif 'quest' in filename:
            saga_data['questlines'] = component_data
        
        return saga_data


def main():
    """Main entry point for orchestrator agent"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m OrchestratorAgent.orchestrator_saga <saga_file_or_directory> [--auto] [--feedback \"your feedback\"]")
        print("\nOptions:")
        print("  --auto        Auto-apply all updates without confirmation")
        print("  --feedback    Provide user feedback for targeted updates")
        sys.exit(1)
    
    saga_path = sys.argv[1]
    auto_apply = '--auto' in sys.argv
    
    # Get feedback if provided
    user_feedback = ""
    if '--feedback' in sys.argv:
        feedback_idx = sys.argv.index('--feedback')
        if feedback_idx + 1 < len(sys.argv):
            user_feedback = sys.argv[feedback_idx + 1]
    
    # Create orchestrator
    orchestrator = OrchestratorAgent()
    
    # Run orchestration
    orchestrator.orchestrate_revision(saga_path, user_feedback=user_feedback, auto_apply=auto_apply)


if __name__ == "__main__":
    main()


