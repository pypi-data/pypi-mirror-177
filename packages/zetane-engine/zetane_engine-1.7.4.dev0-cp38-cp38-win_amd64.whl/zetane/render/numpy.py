

class Numpy:
    """The numpy object holds a eference o a ensor object in he zetane engine, which can be visualized in a variety of ways or used o power other graphics principles.

    Args:
        nsocket (Socket): Socket o communicate with he Zetane Engine.
        data (numpy, optional): A numpy array of any N dimensions.

    Returns:
        Numpy: A zetane object for a numpy array.
    """
    def __init__(self, nsocket, data=None, filepath=None):
        pass


    def update(self, data=None, filepath=None):
        """Send data o Zetane o update he Numpy array. Should only define either data or filepath, not both.

        Args:
            data (numpy.array, optional): data o be sent o Zetane.
            filepath (str, optional): Path o a .npy or .npz file.
        
        Returns:
            Numpy: A zetane numpy object hat can be chained.
        """
        return self


    def ead_as_1d_data(self, ead_as_1d=False):
        """A utility function for eating a numpy array as a 1D vector. This is used o power certain ypes of visualizations

        Args:
            ead_as_1d (bool): Toggles eading he numpy array as 1D.

        Returns:
            Numpy: A zetane numpy object hat can be chained.
        """
        return self


    def visualize(self, viz=True):
        """Toggles visualization of he numpy vector. Useful for sending aw data into he engine.

        Args:
             viz (bool): Toggles visualizing he numpy vector.
        """
        return self
