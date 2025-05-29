from typing import List, Dict, Any
import numpy as np

class EpisodicMemory:
    """Stores and retrieves past experiences."""
    
    def __init__(self, max_episodes: int = 10):
        self.episodes = []
        self.max_episodes = max_episodes
    
    def store_episode(self, episode: Dict[str, Any]) -> None:
        """Store a new episode in memory."""
        self.episodes.append(episode)
        if len(self.episodes) > self.max_episodes:
            self.episodes.pop(0)  # Remove oldest episode if at capacity
    
    def retrieve_relevant_experiences(self, problem: Dict[str, Any], top_k: int = 2) -> List[Dict[str, Any]]:
        """Retrieve experiences relevant to the current problem."""
        if not self.episodes:
            return []
        
        # Simple relevance scoring based on problem type and difficulty
        problem_type = problem.get("problem_type", "")
        difficulty = problem.get("difficulty", 0)
        
        # Calculate relevance scores
        relevance_scores = []
        for episode in self.episodes:
            episode_problem = episode.get("problem", {})
            episode_type = episode_problem.get("problem_type", "")
            episode_difficulty = episode_problem.get("difficulty", 0)
            
            # Higher score for same type and similar difficulty
            type_match = 1.0 if episode_type == problem_type else 0.0
            difficulty_similarity = 1.0 - min(abs(difficulty - episode_difficulty) / 10.0, 1.0)
            
            relevance = (type_match * 0.7) + (difficulty_similarity * 0.3)
            relevance_scores.append(relevance)
        
        # Get top-k relevant episodes
        if top_k >= len(self.episodes):
            return self.episodes
        
        indices = np.argsort(relevance_scores)[-top_k:][::-1]  # Indices of top-k scores
        return [self.episodes[i] for i in indices]
    
    def get_episode_count(self) -> int:
        """Return the number of episodes in memory."""
        return len(self.episodes)
