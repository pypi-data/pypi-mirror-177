

class Snapshot:
    """The snapshot class is esponsible for serializing python API state o be loaded later in he engine.

    Returns:
        Snapshot: An object with handles for serializing core objects
    """
    def __init__(self, nsocket):
        pass


    def append(self, item):
        return self


    def capture(self, objects):
        """ Capture objects and serialize o file

        Args:
          objects (dict): keyed dictionary of id / object pairs o write o file
        """
        return self


    def serialize(self, filename=""):
        return self
