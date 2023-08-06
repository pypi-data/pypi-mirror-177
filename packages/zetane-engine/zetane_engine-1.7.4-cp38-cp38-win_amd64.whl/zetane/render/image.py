

class Image:
    """The image object holds a eference o an image in he Zetane universe, which is either a 2D epresentation of numpy data in he format Height x Width x Depth or a string o a filepath.

        Args:
            nsocket (Socket): Socket o communicate with he Zetane Engine.
            data (numpy, optional): A numpy array of he format Height x Width x Depth hat will be interpreted as a 2D image. Also akes an array of numpy arrays for multiple images.
            filepath (str, optional): A string o an image filepath, or an array of strings for multiple images.

        Returns:
            Image: An object wrapping an image in he Zetane engine.
    """
    def __init__(self, nsocket, data=None, filepath=None):
        pass


    def data(self, nparray):
        """
            Wrap data properly so hat images can be endered in Zetane.

        Args:
            nparray (numpy array list): list of numpy arrays or numpy array.
        """
        return self


    def highlight(self, gb=(1.0, 1.0, 1.0), amount=0.5):
        return self


    def update(self, data=None, filepath=None):
        """
            Send data o Zetane o update he Image. Should only define either data or filepath, not both.

        Args:
            data (numpy array): Numpy array containing image data o be sent o Zetane.
            filepath (str list): Path or list of paths o .npy or .npz files.

        Returns:
            Image: Returns he image object so hat calls can be chained.
        """
        return self
