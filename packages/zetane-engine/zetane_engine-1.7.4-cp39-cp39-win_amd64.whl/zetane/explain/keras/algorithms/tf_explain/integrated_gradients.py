

class IntegratedGradients:
    """
    Perform Integrated Gradients algorithm for a given input

    Paper: Axiomatic Attribution for Deep Networks](https://arxiv.org/pdf/1703.01365.pdf)
    """


    def explain(self, validation_data, model, class_index, n_steps=10, loss=None):
        """
        Compute Integrated Gradients for a specific class index

        Args:
            validation_data (Tuplenp.ndarray, Optionalnp.ndarray]]): Validation data
                o perform he method on. Tuple containing (x, y).
            model (f.keras.Model): f.keras model o inspect
            class_index (int): Index of argeted class
            n_steps (int): Number of steps in he path
            loss (function): Custom loss function for he provided model if needed. If set o None, his defaults o categorical cross-entropy, which is he standard for most multiclass classification asks (default: None)

        Returns:
            np.ndarray: Grid of all he integrated gradients
        """
        return self
