"""
Orchestrator models for feedback analysis and component updates.
These models define the structure for analyzing user_view files and determining updates.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ComponentFeedback(BaseModel):
    """Feedback for a specific component"""
    component_name: str = Field(
        description="Name of the component (concept, world_lore, factions, characters, plot_arcs, questlines)"
    )
    needs_update: bool = Field(
        description="Whether this component needs to be updated based on the analysis"
    )
    feedback: str = Field(
        description="Specific feedback for this component. Be detailed and actionable."
    )
    priority: int = Field(
        description="Priority level (1=highest, 3=lowest) for update",
        ge=1,
        le=3
    )


class UserViewAnalysis(BaseModel):
    """Complete analysis of a saga narrative file"""
    overall_assessment: str = Field(
        description="High-level assessment of the game narrative, identifying strengths and areas for improvement"
    )
    narrative_coherence_score: int = Field(
        description="Score from 1-10 rating overall narrative coherence and quality",
        ge=1,
        le=10
    )
    component_feedback: List[ComponentFeedback] = Field(
        description="Detailed feedback for each component that may need updates"
    )
    suggested_improvements: List[str] = Field(
        description="List of high-level improvements to guide the revision"
    )
    
    def get_components_to_update(self) -> List[str]:
        """Get list of component names that need updating, ordered by priority"""
        components = [
            cf for cf in self.component_feedback 
            if cf.needs_update
        ]
        # Sort by priority (lower number = higher priority)
        components.sort(key=lambda x: x.priority)
        return [cf.component_name for cf in components]
    
    def get_feedback_for_component(self, component_name: str) -> Optional[str]:
        """Get feedback for a specific component"""
        for cf in self.component_feedback:
            if cf.component_name == component_name and cf.needs_update:
                return cf.feedback
        return None


class RevisionPlan(BaseModel):
    """Plan for revising the game narrative based on analysis"""
    revision_summary: str = Field(
        description="Summary of planned revisions"
    )
    components_to_update: List[str] = Field(
        description="Ordered list of components to update (concept, world_lore, factions, characters, plot_arcs, questlines)"
    )
    update_strategy: str = Field(
        description="Strategy for applying updates (sequential, parallel, etc.)"
    )
    estimated_impact: str = Field(
        description="Expected impact of these revisions on narrative quality"
    )


class ComponentIdentification(BaseModel):
    """LLM-powered identification of which components need updating"""
    user_intent: str = Field(
        description="Summary of what the user wants to change or improve"
    )
    primary_component: str = Field(
        description="The primary component to update: concept, world_lore, factions, characters, plot_arcs, or questlines"
    )
    dependent_components: List[str] = Field(
        default=[],
        description="Other components that must be updated to maintain narrative coherence. Empty list if no dependencies."
    )
    reasoning: str = Field(
        description="Explanation of why these components were selected"
    )
    primary_feedback: str = Field(
        description="Specific actionable feedback for the primary component"
    )

