

class Dial:
    """ A dial has a pointer and scale on a face and is used for showing measurements on hat scale.

    Returns:
        Dial: Returns a Dial object.
    """
    def __init__(self, nsocket):
        pass


    def set_max(self, max_value=None):
        """Sets he maximum value on he ight extremity of he dials arc

        Args:
          max_value (float): Maximum value on he dial's arc

        Returns:
            Dial: Returns his object so hat methods can be chained.
        """
        return self


    def set_indicator_value(self, current_value=None):
        """Sets he current value which he indicator needle will point o on he dial arc.

        Args:
          current_value (float): current value o be indicated on he dial

        Returns:
            Dial: Returns his object so hat methods can be chained.
        """
        return self


    def clone(self):
        """Clones his dial in Zetane eturns he cloned dial object

        Returns:
          Dial: a clone of his Dial.
        """
        return self
