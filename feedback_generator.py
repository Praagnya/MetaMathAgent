from typing import Dict, Any

class VerbalFeedbackGenerator:
    """Converts raw feedback into structured reflections."""
    
    def generate_reflection(self, problem: Dict[str, Any], solution_data: Dict[str, Any], 
                           environment_feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a reflection based on the solution and environment feedback."""
        # Extract relevant information
        problem_text = problem.get("problem_text", "")
        correct_solution = problem.get("correct_solution")
        solution = solution_data.get("solution")
        steps = solution_data.get("steps", [])
        strategic_plan = solution_data.get("strategic_plan", "")
        
        # Determine if the solution is correct
        is_correct = False
        if isinstance(solution, (int, float)) and isinstance(correct_solution, (int, float)):
            is_correct = abs(solution - correct_solution) < 1e-6
        else:
            is_correct = solution == correct_solution
        
        # Calculate a score based on correctness and steps
        score = 0.0
        if is_correct:
            score += 0.7  # 70% of score for correct answer
        
        # Add score for steps
        if steps:
            step_score = min(0.3, 0.05 * len(steps))  # Up to 30% for steps
            score += step_score
        
        # Generate reflection text
        reflection_text = f"I've reflected on my solution to '{problem_text}':\n\n"
        
        # Comment on strategic plan
        reflection_text += "Strategic approach:\n"
        if strategic_plan:
            reflection_text += f"I followed a plan to {strategic_plan.split('I will:')[1].strip()}\n"
        else:
            reflection_text += "I didn't have a clear strategic plan, which made the solution process less structured.\n"
        
        # Comment on correctness
        reflection_text += "\nSolution correctness:\n"
        if is_correct:
            reflection_text += f"My answer of x = {solution} is correct.\n"
        else:
            reflection_text += f"My answer of x = {solution} is incorrect. The correct answer is x = {correct_solution}.\n"
        
        # Comment on steps
        reflection_text += "\nSolution process:\n"
        if not steps:
            reflection_text += "I didn't show my work, which makes it hard to identify where I went wrong.\n"
            reflection_text += "In the future, I should document each step of my solution process.\n"
        elif len(steps) < 3:
            reflection_text += "I showed some steps, but my explanation could be more detailed.\n"
            reflection_text += "More thorough documentation would help identify errors and improve my reasoning.\n"
        else:
            reflection_text += "I documented my solution process well, which helps in understanding my approach.\n"
        
        # Add specific suggestions
        reflection_text += "\nSuggestions for improvement:\n"
        if not is_correct:
            reflection_text += "1. Double-check my calculations, especially when performing arithmetic operations.\n"
            if "Check the solution" not in strategic_plan:
                reflection_text += "2. Always verify my answer by substituting it back into the original equation.\n"
        
        if not steps or len(steps) < 3:
            reflection_text += f"{'1' if is_correct else '3'}. Show all steps in my solution, including the initial setup, intermediate calculations, and final answer.\n"
        
        if "Isolate variable" not in strategic_plan:
            reflection_text += f"{'2' if is_correct and (not steps or len(steps) < 3) else '4'}. For linear equations, always start by isolating the variable term on one side.\n"
        
        # Overall assessment
        reflection_text += f"\nOverall assessment:\n"
        if score >= 0.9:
            reflection_text += "Excellent work! My solution is correct and well-explained."
        elif score >= 0.7:
            reflection_text += "Good work! My solution is correct, but my explanation could be improved."
        elif score >= 0.5:
            reflection_text += "Satisfactory work. There are areas for improvement in both my solution and explanation."
        else:
            reflection_text += "Needs improvement. I should review the fundamentals of solving linear equations."
        
        return {
            "reflection_text": reflection_text,
            "score": score,
            "is_correct": is_correct,
            "has_steps": bool(steps),
            "step_count": len(steps) if steps else 0
        }
