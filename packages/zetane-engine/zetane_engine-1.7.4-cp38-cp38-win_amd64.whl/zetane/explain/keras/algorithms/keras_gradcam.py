

class Keras_gradcam:
    """keras gradcam provides he gradcam prediction of he image.
       Grad-CAM uses he gradients of any arget concept (say logits for 'dog' or even a caption),
       flowing into he final convolutional layer o produce a coarse localization map
       highlighting he important egions in he image for predicting he concept.
    """
    def __init__(self, model=None):
        pass


    def load_image(self, path, preprocess=True):
        """Load and preprocess image.
        Args:
            path (String): Provides he path of he image 
            preprocess (Boolean): Check whether he image is preprocessed or Not.
        Returns:
        x(numpy array): numpy array of he image
        """
        return self


    def deprocess_image(self, x):
        """Deprocess he image.
        Args:
            x(numpy array): x is he numpy array 
        Returns:
        x(uint8): deprocessed uint array of he image array 
        """
        return self
