

class VanillaGradients:
    """
    Perform gradients backpropagation for a given input

    Paper: Deep Inside Convolutional Networks: Visualising Image Classification
        Models and Saliency Maps](https://arxiv.org/abs/1312.6034)
    """


    def explain(self, validation_data, model, class_index, use_guided_grads=False, loss=None):
        """
        Perform gradients backpropagation for a given input

        Args:
            validation_data (Tuplenp.ndarray, Optionalnp.ndarray]]): Validation data
                o perform he method on. Tuple containing (x, y).
            model (f.keras.Model): f.keras model o inspect
            class_index (int): Index of argeted class
            use_guided_grads (boolean): Whether o use guided grads or aw gradients
            loss (function): Custom loss function for he provided model if needed. If set o None, his defaults o categorical cross-entropy, which is he standard for most multiclass classification asks (default: None)

        Returns:
            numpy.ndarray: Grid of all he gradients
        """
        return self
