from typing import Dict, List, Any

class MetaThinkingAgent:
    """High-level agent responsible for strategic planning."""
    
    def __init__(self, skill_level: float = 0.7, improvement_rate: float = 0.1):
        self.skill_level = skill_level
        self.improvement_rate = improvement_rate
        self.strategies = {
            "linear_equation": [
                "Isolate variable term by moving constants to the other side",
                "Divide both sides by the coefficient of the variable",
                "Check the solution by substituting back into the original equation"
            ]
        }
    
    def generate_plan(self, problem: Dict[str, Any], past_experiences: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a strategic plan for solving the problem."""
        problem_type = problem.get("problem_type", "")
        
        # Extract insights from past experiences
        insights = self._extract_insights_from_experiences(past_experiences)
        
        # Get base strategies for this problem type
        base_strategies = self.strategies.get(problem_type, [])
        
        # Adjust strategies based on skill level and insights
        if self.skill_level < 0.5:
            # Lower skill level: simpler, more direct approach
            strategies = base_strategies[:1]  # Just the first basic strategy
        elif self.skill_level < 0.8:
            # Medium skill level: standard approach
            strategies = base_strategies[:2]  # First two strategies
        else:
            # High skill level: comprehensive approach
            strategies = base_strategies  # All strategies
        
        # Add insights from past experiences if available
        if insights:
            strategies.extend(insights)
        
        # Generate the plan
        plan = {
            "problem_type": problem_type,
            "strategies": strategies,
            "approach": self._generate_approach_description(problem, strategies)
        }
        
        return plan
    
    def _extract_insights_from_experiences(self, experiences: List[Dict[str, Any]]) -> List[str]:
        """Extract useful insights from past experiences."""
        if not experiences:
            return []
        
        insights = []
        for exp in experiences:
            feedback = exp.get("feedback", {})
            reflection = feedback.get("reflection_text", "")
            
            # Extract suggestions from reflection
            if "suggestion" in reflection.lower():
                suggestion_lines = [line for line in reflection.split('\n') 
                                   if "suggestion" in line.lower()]
                if suggestion_lines:
                    insights.append(suggestion_lines[0].split(":", 1)[1].strip())
        
        return insights[:2]  # Limit to top 2 insights
    
    def _generate_approach_description(self, problem: Dict[str, Any], strategies: List[str]) -> str:
        """Generate a description of the problem-solving approach."""
        problem_text = problem.get("problem_text", "")
        
        approach = f"To solve the problem '{problem_text}', I will:\n"
        for i, strategy in enumerate(strategies):
            approach += f"{i+1}. {strategy}\n"
        
        return approach
    
    def update(self, reward: float) -> None:
        """Update the agent's skill based on reward."""
        if self.skill_level < 1.0:
            improvement = self.improvement_rate * reward
            self.skill_level = min(1.0, self.skill_level + improvement)