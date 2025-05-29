from integration_controller import IntegrationController

def main():
    """Run the ReMA + Reflexion system."""
    system = IntegrationController()
    
    # Run multiple iterations with the same problem to show learning
    print("Running system with the same problem across iterations to demonstrate learning...")
    system.run_multiple_iterations(num_iterations=3, same_problem=True)
    
    # Plot learning curve
    system.plot_learning_curve()
    
    print("\nNow running system with different problems...")
    system = IntegrationController()  # Reset the system
    system.run_multiple_iterations(num_iterations=3, same_problem=False)
    
    # Plot learning curve for different problems
    system.plot_learning_curve()

if __name__ == "__main__":
    main()