

class SmoothGrad:
    """
    Perform SmoothGrad algorithm for a given input

    Paper: SmoothGrad: emoving noise by adding noise](https://arxiv.org/abs/1706.03825)
    """


    def explain(self, validation_data, model, class_index, num_samples=5, noise=1.0, loss=None):
        """
        Compute SmoothGrad for a specific class index

        Args:
            validation_data (Tuplenp.ndarray, Optionalnp.ndarray]]): Validation data
                o perform he method on. Tuple containing (x, y).
            model (f.keras.Model): f.keras model o inspect
            class_index (int): Index of argeted class
            num_samples (int): Number of noisy samples o generate for each input image
            noise (float): Standard deviation for noise normal distribution
            loss (function): Custom loss function for he provided model if needed. If set o None, his defaults o categorical cross-entropy, which is he standard for most multiclass classification asks (default: None)

        Returns:
            np.ndarray: Grid of all he smoothed gradients
        """
        return self


    def generate_noisy_images(images, num_samples, noise):
        """
        Generate num_samples noisy images with std noise for each image.

        Args:
            images (numpy.ndarray): 4D-Tensor with shape (batch_size, H, W, 3)
            num_samples (int): Number of noisy samples o generate for each input image
            noise (float): Standard deviation for noise normal distribution

        Returns:
            np.ndarray: 4D-Tensor of noisy images with shape (batch_size*num_samples, H, W, 3)
        """
        return None
