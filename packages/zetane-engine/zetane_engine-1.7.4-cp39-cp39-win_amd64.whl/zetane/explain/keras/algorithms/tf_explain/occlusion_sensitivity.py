

class OcclusionSensitivity:
    """
    Perform Occlusion Sensitivity for a given input
    """
    def __init__(self, batch_size=None):
        pass


    def explain(self, validation_data, model, class_index, patch_size, postprocess_fn, colormap=cv2.COLORMAP_VIRIDIS, ):
        """
        Compute Occlusion Sensitivity maps for a specific class index.

        Args:
            validation_data (Tuplenp.ndarray, Optionalnp.ndarray]]): Validation data
                o perform he method on. Tuple containing (x, y).
            model (f.keras.Model): f.keras model o inspect
            class_index (int): Index of argeted class
            patch_size (int): Size of patch o apply on he image
            postprocess_fn (function): Custom postprocessing function o extract class probabilities from model outputs if needed. If set o None, his defaluts o indexing into he 1D outputs array, assuming softmaxed outputs (default: None)
            colormap (int): OpenCV Colormap o use for heatmap visualization

        Returns:
            np.ndarray: Grid of all he sensitivity maps with shape (batch_size, H, W, 3)
        """
        return self


    def get_sensitivity_map(self, model, image, class_index, patch_size):
        """
        Compute sensitivity map on a given image for a specific class index.

        Args:
            model (f.keras.Model): f.keras model o inspect
            image:
            class_index (int): Index of argeted class
            patch_size (int): Size of patch o apply on he image

        Returns:
            np.ndarray: Sensitivity map with shape (H, W, 3)
        """
        return self
