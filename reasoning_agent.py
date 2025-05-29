import random
import re
from typing import Dict, Any


class ReasoningAgent:
    """Low-level agent responsible for detailed execution."""
    
    def __init__(self, skill_level: float = 0.6, improvement_rate: float = 0.1):
        self.skill_level = skill_level
        self.improvement_rate = improvement_rate
        self.error_probability = 1.0 - self.skill_level
        self.step_verbosity = 0.7  # Probability of showing intermediate steps
    
    def solve_problem(self, problem: Dict[str, Any], strategic_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Solve the problem following the strategic plan."""
        if problem["problem_type"] == "linear_equation":
            return self._solve_linear_equation(problem, strategic_plan)
        else:
            return {"error": "Unsupported problem type"}
    
    def _solve_linear_equation(self, problem: Dict[str, Any], strategic_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Solve a linear equation following the strategic plan."""
        equation = problem["equation"]
        # Parse the equation
        match = re.match(r"(\d+)x \+ (\d+) = (\d+)", equation)
        if not match:
            return {"error": "Failed to parse equation"}
        
        a, b, c = map(int, match.groups())
        
        # Determine if we'll make an error based on skill level
        make_error = random.random() < self.error_probability
        
        # Determine if we'll show steps based on verbosity
        show_steps = random.random() < self.step_verbosity
        
        steps = []
        
        # Follow the strategic plan
        strategies = strategic_plan.get("strategies", [])
        
        if show_steps:
            steps.append(f"Starting with the equation: {a}x + {b} = {c}")
            
            # Strategy 1: Isolate variable term
            if strategies and "Isolate variable" in strategies[0]:
                steps.append(f"Following strategy: {strategies[0]}")
                steps.append(f"Subtracting {b} from both sides: {a}x = {c} - {b}")
                
                # Possible error in subtraction
                if make_error and random.random() < 0.5:
                    error_c_minus_b = c - b + random.choice([-1, 1])
                    steps.append(f"This gives us: {a}x = {error_c_minus_b}")
                    c_minus_b = error_c_minus_b
                else:
                    steps.append(f"This gives us: {a}x = {c - b}")
                    c_minus_b = c - b
            else:
                # No strategy for isolation, just do it
                steps.append(f"Subtracting {b} from both sides: {a}x = {c - b}")
                c_minus_b = c - b
            
            # Strategy 2: Divide by coefficient
            if len(strategies) > 1 and "Divide both sides" in strategies[1]:
                steps.append(f"Following strategy: {strategies[1]}")
                steps.append(f"Dividing both sides by {a}: x = {c_minus_b} / {a}")
                
                # Possible error in division
                if make_error and random.random() < 0.5:
                    error_x = c_minus_b / a + random.choice([-1, 1])
                    steps.append(f"Therefore, x = {error_x}")
                    solution = error_x
                else:
                    steps.append(f"Therefore, x = {c_minus_b / a}")
                    solution = c_minus_b / a
            else:
                # No strategy for division, just do it
                steps.append(f"Dividing both sides by {a}: x = {c_minus_b / a}")
                solution = c_minus_b / a
            
            # Strategy 3: Check solution
            if len(strategies) > 2 and "Check the solution" in strategies[2]:
                steps.append(f"Following strategy: {strategies[2]}")
                check_result = a * solution + b
                steps.append(f"Checking: {a} × {solution} + {b} = {check_result}")
                
                if abs(check_result - c) < 0.001:
                    steps.append(f"The solution checks out: {check_result} ≈ {c}")
                else:
                    steps.append(f"The solution doesn't check out: {check_result} ≠ {c}")
                    steps.append(f"Let me recalculate...")
                    solution = (c - b) / a  # Correct the solution
                    steps.append(f"The correct solution is x = {solution}")
        else:
            # Just give the answer with possible error
            if make_error:
                solution = (c - b) / a + random.choice([-1, 1])
            else:
                solution = (c - b) / a
        
        # Ensure solution is an integer if the correct answer is an integer
        if isinstance(problem["correct_solution"], int):
            solution = round(solution)
        
        return {
            "problem": problem["problem_text"],
            "strategic_plan": strategic_plan["approach"],
            "steps": steps,
            "solution": solution,
            "correct_solution": problem["correct_solution"]
        }
    
    def update(self, reward: float) -> None:
        """Update the agent's skill based on reward."""
        if self.skill_level < 1.0:
            improvement = self.improvement_rate * reward
            self.skill_level = min(1.0, self.skill_level + improvement)
            self.error_probability = 1.0 - self.skill_level
            
            # Also increase step verbosity as skill improves
            self.step_verbosity = min(1.0, self.step_verbosity + (improvement * 0.5))
