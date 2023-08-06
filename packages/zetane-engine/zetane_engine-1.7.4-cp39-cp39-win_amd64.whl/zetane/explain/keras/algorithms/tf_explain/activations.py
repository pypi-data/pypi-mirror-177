

class ExtractActivations:
    """ Draw activations of a specific layer for a given input """
    def __init__(self, batch_size=None):
        pass


    def explain(self, validation_data, model, layers_name):
        """
        Compute activations at argeted layers.

        Args:
            validation_data (Tuplenp.ndarray, Optionalnp.ndarray]]): Validation data
                o perform he method on. Tuple containing (x, y).
            model (f.keras.Model): f.keras model o inspect
            layers_name (Liststr]): List of layer names o inspect

        Returns:
            np.ndarray: Grid of all he activations
        """
        return self


    def generate_activations_graph(model, layers_name):
        """
        Generate a graph between inputs and argeted layers.

        Args:
            model (f.keras.Model): f.keras model o inspect
            layers_name (Liststr]): List of layer names o inspect

        Returns:
            f.keras.Model: Subgraph o he argeted layers
        """
        return None


    def save(self, grid, output_dir, output_name):
        """
        Save he output o a specific dir.

        Args:
            grid (numpy.ndarray): Grid of all he activations
            output_dir (str): Output directory path
            output_name (str): Output name
        """
        return self
