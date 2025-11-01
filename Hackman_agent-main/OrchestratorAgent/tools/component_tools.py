"""
LangChain tools for the orchestrator agent to interact with saga narrative components.
These tools allow the ReAct agent to analyze and update specific components.
"""
from typing import Dict, Any, List, Optional
from langchain.tools import BaseTool
from pydantic import Field


class AnalyzeComponentTool(BaseTool):
    """Tool to analyze a specific narrative component and determine if it needs updating."""
    
    name: str = "analyze_component"
    description: str = """
    Analyze a specific saga narrative component to determine if it needs updating based on user feedback.
    
    Input should be a JSON string with:
    - component_name: One of 'concept', 'world_lore', 'factions', 'characters', 'plot_arcs', 'questlines'
    - user_feedback: The user's feedback text
    - current_state: Current state of the component
    
    Returns analysis indicating if update is needed and why.
    """
    
    saga_data: Dict[str, Any] = Field(default_factory=dict)
    
    def _run(self, component_name: str, user_feedback: str = "") -> str:
        """Analyze if a component needs updating."""
        import json
        
        # Get current component state
        component_data = self.saga_data.get(component_name, None)
        
        # Analyze based on feedback keywords and current state
        analysis = {
            "component": component_name,
            "needs_update": False,
            "reasoning": "",
            "current_count": 0
        }
        
        feedback_lower = user_feedback.lower()
        
        # Concept-specific analysis
        if component_name == "concept":
            concept = self.saga_data.get('concept', {})
            concept_keywords = ['concept', 'game', 'core loop', 'mechanics', 'usp', 'genre', 
                               'elevator pitch', 'gameplay', 'monetization']
            
            if any(keyword in feedback_lower for keyword in concept_keywords):
                analysis["needs_update"] = True
                analysis["reasoning"] = f"User feedback mentions game concept changes. Current title: {concept.get('title', 'N/A')}"
            else:
                analysis["reasoning"] = "No concept-related keywords detected in feedback"
        
        # World lore-specific analysis
        elif component_name == "world_lore":
            world_lore = self.saga_data.get('world_lore', {})
            lore_keywords = ['world', 'lore', 'history', 'culture', 'setting', 'geography', 
                            'theme', 'mythology', 'background', 'dystopian', 'utopian']
            
            if any(keyword in feedback_lower for keyword in lore_keywords):
                analysis["needs_update"] = True
                analysis["reasoning"] = f"User feedback mentions world lore changes. Current world: {world_lore.get('world_name', 'N/A')}"
            else:
                analysis["reasoning"] = "No world lore keywords detected in feedback"
        
        # Factions-specific analysis
        elif component_name == "factions":
            current_factions = self.saga_data.get('factions', [])
            analysis["current_count"] = len(current_factions)
            
            faction_keywords = ['faction', 'group', 'organization', 'guild', 'clan', 'house',
                               'alliance', 'council', 'syndicate', 'gang', 'tribe']
            
            if any(keyword in feedback_lower for keyword in faction_keywords):
                analysis["needs_update"] = True
                analysis["reasoning"] = f"User feedback mentions faction changes. Current factions: {[f.get('name', 'Unnamed') for f in current_factions]}"
            else:
                analysis["reasoning"] = "No faction-related keywords detected"
        
        # Character-specific analysis
        elif component_name == "characters":
            current_characters = self.saga_data.get('characters', [])
            analysis["current_count"] = len(current_characters)
            
            char_keywords = ['character', 'person', 'protagonist', 'npc', 'hero', 'villain',
                            'leader', 'merchant', 'warrior', 'mage', 'add', 'create', 'named']
            
            if any(keyword in feedback_lower for keyword in char_keywords):
                analysis["needs_update"] = True
                analysis["reasoning"] = f"User feedback mentions character changes. Current characters: {[c.get('name', 'Unnamed') for c in current_characters]}"
            else:
                analysis["reasoning"] = "No character-related keywords detected"
        
        # Plot arcs-specific analysis
        elif component_name == "plot_arcs":
            current_arcs = self.saga_data.get('plot_arcs', [])
            analysis["current_count"] = len(current_arcs)
            
            arc_keywords = ['plot', 'arc', 'story', 'narrative', 'storyline', 'campaign',
                           'chapter', 'act', 'dramatic', 'conflict', 'stakes']
            
            if any(keyword in feedback_lower for keyword in arc_keywords):
                analysis["needs_update"] = True
                analysis["reasoning"] = f"User feedback mentions plot arc changes. Current arcs: {[a.get('arc_name', 'Unnamed') for a in current_arcs]}"
            else:
                analysis["reasoning"] = "No plot arc keywords detected"
        
        # Questlines-specific analysis
        elif component_name == "questlines":
            current_quests = self.saga_data.get('questlines', [])
            analysis["current_count"] = len(current_quests)
            
            quest_keywords = ['quest', 'mission', 'task', 'objective', 'challenge', 'side quest',
                             'main quest', 'questline', 'reward', 'achievement']
            
            if any(keyword in feedback_lower for keyword in quest_keywords):
                analysis["needs_update"] = True
                analysis["reasoning"] = f"User feedback mentions questline changes. Current quests: {[q.get('quest_name', 'Unnamed') for q in current_quests]}"
            else:
                analysis["reasoning"] = "No questline keywords detected"
        
        return json.dumps(analysis, indent=2)
    
    async def _arun(self, *args, **kwargs):
        """Async version."""
        raise NotImplementedError("Async not implemented")


class CheckDependenciesTool(BaseTool):
    """Tool to check which other components depend on a given component."""
    
    name: str = "check_dependencies"
    description: str = """
    Check which other saga narrative components depend on a given component.
    
    Input should be the component name: 'concept', 'world_lore', 'factions', 'characters', 'plot_arcs', 'questlines'
    
    Returns a list of dependent components that must be updated to maintain coherence.
    """
    
    def _run(self, component_name: str) -> str:
        """Check component dependencies."""
        import json
        
        dependency_map = {
            "concept": {
                "dependent_components": ["world_lore", "factions", "characters", "plot_arcs", "questlines"],
                "reasoning": "Concept changes affect the entire narrative structure"
            },
            "world_lore": {
                "dependent_components": ["factions", "characters", "plot_arcs"],
                "reasoning": "World lore establishes the foundation for factions, characters, and story arcs"
            },
            "factions": {
                "dependent_components": ["characters", "plot_arcs"],
                "reasoning": "Faction changes affect character affiliations and political plot arcs"
            },
            "characters": {
                "dependent_components": ["plot_arcs", "questlines"],
                "reasoning": "New/changed characters need involvement in arcs and quests"
            },
            "plot_arcs": {
                "dependent_components": ["questlines"],
                "reasoning": "Plot arcs typically manifest as questlines for player interaction"
            },
            "questlines": {
                "dependent_components": [],
                "reasoning": "Questlines are the final implementation and typically don't cascade further"
            }
        }
        
        result = dependency_map.get(component_name, {
            "dependent_components": [],
            "reasoning": "Unknown component"
        })
        
        return json.dumps(result, indent=2)
    
    async def _arun(self, *args, **kwargs):
        """Async version."""
        raise NotImplementedError("Async not implemented")


class GetComponentInfoTool(BaseTool):
    """Tool to get detailed information about a narrative component."""
    
    name: str = "get_component_info"
    description: str = """
    Get detailed information about a specific saga narrative component.
    
    Input should be the component name: 'concept', 'world_lore', 'factions', 'characters', 'plot_arcs', 'questlines'
    
    Returns current state and metadata about the component.
    """
    
    saga_data: Dict[str, Any] = Field(default_factory=dict)
    
    def _run(self, component_name: str) -> str:
        """Get component information."""
        import json
        
        info = {
            "component": component_name,
            "exists": False,
            "details": {}
        }
        
        if component_name == "concept":
            concept = self.saga_data.get('concept', {})
            info["exists"] = bool(concept)
            info["details"] = {
                "title": concept.get('title', 'N/A'),
                "genre": concept.get('genre', 'N/A'),
                "elevator_pitch": concept.get('elevator_pitch', 'N/A')[:200],
                "usp": concept.get('usp', 'N/A')[:200]
            }
        
        elif component_name == "world_lore":
            world_lore = self.saga_data.get('world_lore', {})
            info["exists"] = bool(world_lore)
            info["details"] = {
                "world_name": world_lore.get('world_name', 'N/A'),
                "themes": world_lore.get('key_themes', []),
                "history_length": len(world_lore.get('history', '')),
                "culture_length": len(world_lore.get('culture', ''))
            }
        
        elif component_name == "factions":
            factions = self.saga_data.get('factions', [])
            info["exists"] = len(factions) > 0
            info["details"] = {
                "count": len(factions),
                "names": [f.get('name', 'Unnamed') for f in factions],
                "influence_levels": [f.get('influence_level', 'N/A') for f in factions]
            }
        
        elif component_name == "characters":
            characters = self.saga_data.get('characters', [])
            info["exists"] = len(characters) > 0
            info["details"] = {
                "count": len(characters),
                "names": [c.get('name', 'Unnamed') for c in characters],
                "roles": [c.get('role', 'unknown') for c in characters],
                "factions": [c.get('faction_affiliation', 'None') for c in characters]
            }
        
        elif component_name == "plot_arcs":
            arcs = self.saga_data.get('plot_arcs', [])
            info["exists"] = len(arcs) > 0
            info["details"] = {
                "count": len(arcs),
                "arc_names": [a.get('arc_name', 'Unnamed') for a in arcs],
                "arc_types": [a.get('arc_type', 'N/A') for a in arcs]
            }
        
        elif component_name == "questlines":
            quests = self.saga_data.get('questlines', [])
            info["exists"] = len(quests) > 0
            info["details"] = {
                "count": len(quests),
                "quest_names": [q.get('quest_name', 'Unnamed') for q in quests],
                "quest_types": [q.get('quest_type', 'N/A') for q in quests]
            }
        
        return json.dumps(info, indent=2)
    
    async def _arun(self, *args, **kwargs):
        """Async version."""
        raise NotImplementedError("Async not implemented")
