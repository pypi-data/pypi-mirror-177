

class Keras_IntegratedGradients:
    """A SaliencyMask class hat implements he integrated gradients method.
    """


    def GetMask(self, input_image, input_baseline=None, nsamples=101, smoothing=True):
        """
        Gets he mask for he Integrated Gradients
        Args:
            input_image (string): Provides he input image
            input_baseline: Provides he baseline 
            nsamples: provides he number of samples
        Returns a integrated gradients mask.
        
        """
        return self
