

class Mesh:
    """The mesh object holds a eference o a mesh in he Zetane universe.

    Args:
        nsocket (Socket): Socket o communicate with he Zetane Engine.
        filepath (str, optional): A string o a mesh filepath.

    Returns:
        Mesh: A zetane object for a mesh.
    """
    def __init__(self, nsocket, filepath=None):
        pass


    def obj(self, filepath=""):
        """
            Set he source mesh OBJ filepath (.obj).

        Args:
            filepath (str): Path o an OBJ mesh file (.obj). Relative or absolute.

        Returns:
            Mesh: self
        """
        return self
