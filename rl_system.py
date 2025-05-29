from typing import Dict, Any
from meta_thinking_agent import MetaThinkingAgent
from reasoning_agent import ReasoningAgent

class ReinforcementLearningSystem:
    """Updates agents based on performance."""
    
    def calculate_rewards(self, reflection: Dict[str, Any]) -> Dict[str, float]:
        """Calculate rewards for each agent based on the reflection."""
        score = reflection.get("score", 0.0)
        is_correct = reflection.get("is_correct", False)
        has_steps = reflection.get("has_steps", False)
        step_count = reflection.get("step_count", 0)
        
        # Base reward from overall score
        base_reward = score
        
        # Meta-thinking agent reward: more weight on correctness
        meta_reward = base_reward * 1.2 if is_correct else base_reward * 0.8
        
        # Reasoning agent reward: balance between correctness and steps
        reasoning_reward = base_reward
        if has_steps:
            reasoning_reward *= 1.0 + (min(step_count, 5) / 10.0)  # Bonus for steps, up to +0.5
        
        return {
            "meta_agent": meta_reward,
            "reasoning_agent": reasoning_reward,
            "base_reward": base_reward
        }
    
    def update_agents(self, meta_agent: MetaThinkingAgent, reasoning_agent: ReasoningAgent, 
                     rewards: Dict[str, float]) -> None:
        """Update agents based on calculated rewards."""
        meta_agent.update(rewards["meta_agent"])
        reasoning_agent.update(rewards["reasoning_agent"])