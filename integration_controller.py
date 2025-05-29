import time  
from typing import Dict, Any, List  
from problem_generator import MathProblemGenerator
from meta_thinking_agent import MetaThinkingAgent
from reasoning_agent import ReasoningAgent
from feedback_generator import VerbalFeedbackGenerator
from episodic_memory import EpisodicMemory
from rl_system import ReinforcementLearningSystem


class IntegrationController:
    """Manages the overall system workflow."""
    
    def __init__(self):
        self.problem_generator = MathProblemGenerator()
        self.meta_agent = MetaThinkingAgent(skill_level=0.6)
        self.reasoning_agent = ReasoningAgent(skill_level=0.5)
        self.feedback_generator = VerbalFeedbackGenerator()
        self.rl_system = ReinforcementLearningSystem()
        self.episodic_memory = EpisodicMemory()
        self.history = []
    
    def process_task(self, problem=None):
        """Process a single task through the system."""
        # Generate a problem if none provided
        if problem is None:
            problem = self.problem_generator.generate_linear_equation()
        
        print(f"Problem: {problem['problem_text']}")
        print(f"Correct solution: {problem['correct_solution']}")
        
        # Step 1-2: Retrieve relevant experiences and generate strategic plan
        print("\n--- Meta-Thinking Agent ---")
        past_experiences = self.episodic_memory.retrieve_relevant_experiences(problem)
        if past_experiences:
            print(f"Retrieved {len(past_experiences)} relevant past experiences")
        else:
            print("No relevant past experiences found")
        
        strategic_plan = self.meta_agent.generate_plan(problem, past_experiences)
        print(f"Strategic Plan:\n{strategic_plan['approach']}")
        
        # Step 3-4: Reasoning agent solves the problem
        print("\n--- Reasoning Agent ---")
        solution_data = self.reasoning_agent.solve_problem(problem, strategic_plan)
        print(f"Solution: {solution_data['solution']}")
        if solution_data.get("steps"):
            print("Steps:")
            for step in solution_data["steps"]:
                print(f"  {step}")
        else:
            print("No steps provided.")
        
        # Step 5: Environment feedback (simulated)
        environment_feedback = self._simulate_environment_feedback(problem, solution_data)
        
        # Step 6-7: Generate reflection and store in episodic memory
        print("\n--- Verbal Feedback Generator ---")
        reflection = self.feedback_generator.generate_reflection(
            problem, solution_data, environment_feedback)
        print(reflection["reflection_text"])
        
        # Store episode in memory
        episode = {
            "problem": problem,
            "strategic_plan": strategic_plan,
            "solution": solution_data,
            "environment_feedback": environment_feedback,
            "feedback": reflection,
            "timestamp": time.time()
        }
        self.episodic_memory.store_episode(episode)
        print(f"\nEpisode stored in memory (total episodes: {self.episodic_memory.get_episode_count()})")
        
        # Step 9-11: Calculate rewards and update agents
        rewards = self.rl_system.calculate_rewards(reflection)
        self.rl_system.update_agents(self.meta_agent, self.reasoning_agent, rewards)
        
        print(f"\nRewards: Meta-Agent: {rewards['meta_agent']:.2f}, Reasoning Agent: {rewards['reasoning_agent']:.2f}")
        print(f"Updated skill levels: Meta-Agent: {self.meta_agent.skill_level:.2f}, Reasoning Agent: {self.reasoning_agent.skill_level:.2f}")
        
        # Store iteration in history
        self.history.append({
            "problem": problem,
            "solution": solution_data,
            "reflection": reflection,
            "rewards": rewards,
            "meta_skill": self.meta_agent.skill_level,
            "reasoning_skill": self.reasoning_agent.skill_level
        })
        
        return {
            "problem": problem,
            "strategic_plan": strategic_plan,
            "solution": solution_data,
            "reflection": reflection,
            "rewards": rewards
        }
    
    def _simulate_environment_feedback(self, problem: Dict[str, Any], solution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate feedback from the environment."""
        correct_solution = problem.get("correct_solution")
        solution = solution_data.get("solution")
        
        # Check if the solution is correct
        is_correct = False
        if isinstance(solution, (int, float)) and isinstance(correct_solution, (int, float)):
            is_correct = abs(solution - correct_solution) < 1e-6
        else:
            is_correct = solution == correct_solution
        
        return {
            "is_correct": is_correct,
            "correct_solution": correct_solution
        }
    
    def run_multiple_iterations(self, num_iterations=3, same_problem=False):
        """Run multiple iterations, optionally using the same problem."""
        results = []
        problem = None
        
        if same_problem:
            problem = self.problem_generator.generate_linear_equation()
            print(f"Generated problem for all iterations: {problem['problem_text']}")
        
        for i in range(num_iterations):
            print(f"\n{'='*50}\nIteration {i+1}/{num_iterations}\n{'='*50}")
            result = self.process_task(problem)
            results.append(result)
            
            # If using different problems, set problem to None to generate a new one
            if not same_problem:
                problem = None
        
        return results
    
    def plot_learning_curve(self):
        """Plot the learning curve of the agents."""
        try:
            import matplotlib.pyplot as plt
            
            iterations = range(1, len(self.history) + 1)
            meta_skills = [h["meta_skill"] for h in self.history]
            reasoning_skills = [h["reasoning_skill"] for h in self.history]
            scores = [h["reflection"]["score"] for h in self.history]
            
            plt.figure(figsize=(10, 6))
            plt.plot(iterations, meta_skills, 'b-', label='Meta-Agent Skill')
            plt.plot(iterations, reasoning_skills, 'g-', label='Reasoning Agent Skill')
            plt.plot(iterations, scores, 'r-', label='Solution Score')
            plt.xlabel('Iteration')
            plt.ylabel('Score / Skill Level')
            plt.title('Learning Curve')
            plt.legend()
            plt.grid(True)
            plt.savefig('rema_reflexion_learning_curve.png')
            plt.close()
            
            print("Learning curve saved as 'rema_reflexion_learning_curve.png'")
        except ImportError:
            print("Matplotlib not available. Cannot plot learning curve.")

