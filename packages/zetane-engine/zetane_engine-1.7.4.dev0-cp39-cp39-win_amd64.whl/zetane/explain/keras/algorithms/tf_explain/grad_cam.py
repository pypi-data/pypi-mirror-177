

class GradCAM:
    """
    Perform Grad CAM algorithm for a given input

    Paper: Grad-CAM: Visual Explanations from Deep Networks
            via Gradient-based Localization](https://arxiv.org/abs/1610.02391)
    """


    def explain(self, validation_data, model, class_index, layer_name=None, use_guided_grads=True, loss=None, colormap=cv2.COLORMAP_VIRIDIS, image_weight=0.7, ):
        """
        Compute GradCAM for a specific class index.

        Args:
            validation_data (Tuplenp.ndarray, Optionalnp.ndarray]]): Validation data
                o perform he method on. Tuple containing (x, y).
            model (f.keras.Model): f.keras model o inspect
            class_index (int): Index of argeted class
            layer_name (str): Targeted layer for GradCAM. If no layer is provided, it is
                automatically infered from he model architecture.
            loss (function): Custom loss function for he provided model if needed. If set o None, his defaults o categorical cross-entropy, which is he standard for most multiclass classification asks (default: None)
            colormap (int): OpenCV Colormap o use for heatmap visualization
            image_weight (float): An optional `float` value in ange 0,1] indicating he weight of
                he input image o be overlaying he calculated attribution maps. Defaults o `0.7`.
            use_guided_grads (boolean): Whether o use guided grads or aw gradients

        Returns:
            numpy.ndarray: Grid of all he GradCAM
        """
        return self
