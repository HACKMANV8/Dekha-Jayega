"""
ReAct-pattern orchestrator agent - simplified implementation.
This agent uses ReAct reasoning pattern (Thought -> Action -> Observation)
with direct LLM calls instead of complex LangChain agent framework.
"""
from typing import Dict, Any, List, Optional
import json

from OrchestratorAgent.tools.component_tools import (
    AnalyzeComponentTool,
    CheckDependenciesTool,
    GetComponentInfoTool
)
from SagaAgent.services.llm_service import LLMService


class ReactOrchestratorAgent:
    """
    ReAct-based orchestrator that reasons about component updates.
    
    Uses the ReAct (Reasoning + Acting) pattern:
    1. Thought: Reasons about what to do
    2. Action: Takes an action (analyze component, check dependencies, etc.)
    3. Observation: Observes the result
    4. Repeats until it has a plan
    """
    
    def __init__(self, state: Dict[str, Any], user_view_data: Dict[str, Any]):
        """
        Initialize the ReAct orchestrator.
        
        Args:
            state: Current story state
            user_view_data: Loaded user_view JSON data
        """
        self.state = state
        self.user_view_data = user_view_data
        
        # Initialize LLM
        self.llm = self._create_llm()
        
        # Initialize tools
        self.analyze_tool = AnalyzeComponentTool(user_view_data=user_view_data)
        self.dependency_tool = CheckDependenciesTool()
        self.info_tool = GetComponentInfoTool(user_view_data=user_view_data)
    
    def _create_llm(self):
        """Create LLM instance for ReAct reasoning."""
        # Use analytical temperature for reasoning
        return LLMService.create_llm(self.state, creative=False)
    
    def _create_react_prompt(self, user_feedback: str) -> str:
        """Create the ReAct prompt for reasoning about component updates."""
        
        prompt = f"""You are an intelligent story orchestrator agent using ReAct (Reasoning + Acting) pattern.

User Feedback: "{user_feedback}"

Current Story State:
- Title: {self.user_view_data.get('title', 'Unknown')}
- Genre: {self.user_view_data.get('genre', 'Unknown')}
- Characters: {len(self.user_view_data.get('characters', []))} defined
- Locations: {len(self.user_view_data.get('locations', []))} defined
- Scenes: {len(self.user_view_data.get('scenes', []))} defined

Your task: Determine which components to update using ReAct pattern.

Available Components:
- draft: Core story narrative
- characters: Character definitions
- dialogue: Character dialogue/narration
- locations: Physical settings
- visual_lookbook: Visual style/cinematography
- scenes: Scene-by-scene breakdown

Analyze the feedback step-by-step and determine:
1. Which component is the PRIMARY target?
2. Which components DEPEND on the primary and must also update?
3. What is your REASONING?

Be conservative - only update what's necessary. For location changes, consider current locations.

Provide your answer as JSON:
{{
  "primary_component": "component_name",
  "dependent_components": ["dep1", "dep2"],
  "reasoning": "explanation"
}}"""
        
        return prompt
    
    def _use_tool(self, tool_name: str, tool_input: str) -> str:
        """Execute a tool and return observation."""
        if tool_name == "analyze_component":
            parts = tool_input.split('|')
            component = parts[0].strip() if parts else tool_input
            feedback = parts[1].strip() if len(parts) > 1 else ""
            return self.analyze_tool._run(component, feedback)
        elif tool_name == "check_dependencies":
            return self.dependency_tool._run(tool_input.strip())
        elif tool_name == "get_component_info":
            return self.info_tool._run(tool_input.strip())
        else:
            return json.dumps({"error": "Unknown tool"})
    
    def analyze_feedback(self, user_feedback: str) -> Dict[str, Any]:
        """
        Analyze user feedback using ReAct-inspired reasoning.
        
        Args:
            user_feedback: User's feedback about the story
            
        Returns:
            Dictionary with primary_component, dependent_components, and reasoning
        """
        print(f"\n{'='*70}")
        print(f"REACT-PATTERN REASONING")
        print(f"{'='*70}")
        print(f"User Feedback: {user_feedback}")
        print(f"{'='*70}\n")
        
        try:
            # Create prompt
            prompt = self._create_react_prompt(user_feedback)
            
            # Get LLM response
            response = self.llm.invoke(prompt)
            
            # Extract content
            if hasattr(response, 'content'):
                output = response.content
            else:
                output = str(response)
            
            print("LLM Response:")
            print(output)
            print()
            
            # Parse JSON from output
            try:
                # Look for JSON in the output
                if '{' in output:
                    json_start = output.index('{')
                    json_end = output.rindex('}') + 1
                    json_str = output[json_start:json_end]
                    decision = json.loads(json_str)
                else:
                    decision = json.loads(output)
            except json.JSONDecodeError:
                print("[WARNING] Could not parse JSON, using fallback analysis")
                return self._fallback_analysis(user_feedback)
            
            print(f"\n{'='*70}")
            print(f"REACT DECISION")
            print(f"{'='*70}")
            print(f"Primary Component: {decision.get('primary_component')}")
            print(f"Dependent Components: {decision.get('dependent_components', [])}")
            print(f"Reasoning: {decision.get('reasoning')}")
            print(f"{'='*70}\n")
            
            return decision
            
        except Exception as e:
            print(f"[ERROR] ReAct error: {e}")
            print("Using fallback analysis...")
            return self._fallback_analysis(user_feedback)
    
    def _fallback_analysis(self, user_feedback: str) -> Dict[str, Any]:
        """Fallback analysis using simple keyword matching."""
        feedback_lower = user_feedback.lower()
        
        # Check for location keywords
        location_keywords = ['location', 'place', 'setting', 'cafe', 'park', 'shop', 'change the']
        if any(kw in feedback_lower for kw in location_keywords):
            return {
                "primary_component": "locations",
                "dependent_components": [],  # CONSERVATIVE: No auto-dependencies
                "reasoning": "Fallback: Detected location-related keywords (updating location only)"
            }
        
        # Check for character keywords
        char_keywords = ['character', 'person', 'add', 'named']
        if any(kw in feedback_lower for kw in char_keywords):
            return {
                "primary_component": "characters",
                "dependent_components": [],  # CONSERVATIVE: No auto-dependencies
                "reasoning": "Fallback: Detected character-related keywords (adding character only)"
            }
        
        # Default to draft
        return {
            "primary_component": "draft",
            "dependent_components": [],  # CONSERVATIVE: No auto-dependencies
            "reasoning": "Fallback: General story feedback (updating draft only)"
        }

