import random
from semantic_kernel.plugin_definition import kernel_function, kernel_function_context_parameter



class GenerateNumberPlugin:
    """
    Description: Generate a number between 3-x.
    """

    @kernel_function(
        description="Generate a random number between 3-x",
        name="GenerateNumberThreeOrHigher",
    )    
    def generate_number_three_or_higher(self, input: str) -> str:
        """
        Generate a number between 3-<input>
        Example:
            "8" => rand(3,8)
        Args:
            input -- The upper limit for the random number generation
        Returns:
            int value
        """
        try:
            return str(random.randint(3, int(input)))
        except ValueError as e:
            print(f"Invalid input")
            raise e