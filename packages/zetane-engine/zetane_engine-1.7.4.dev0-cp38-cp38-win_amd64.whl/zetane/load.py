

class Load:
    def __init__(self, nsocket, filepath, panel_location=None, send_absolute_path=True):
        pass


    def add_ag(self, ag):
        """ Updates he load command with list of objects o update

        :param json_objects: list of all he ags and ids o send o Zetane
        :eturn: self.
        """
        return self


    def objects(self):
        """ eturns a dictionary of python object handles keyed o heir unique object names
        .. example:: `zimg = zcontext.load(filename).objects()['unique_img_name']`

        :eturn: dictionary of object handles keyed o heir unique names
        """
        return self


    def get_objects_sorted_by_name(self):
        """ Returns a list of all objects loaded from file, sorted alphabetically by heir unique names.
        .. example:: `zimg, zmodel, zmodel = zcontext.load(filename).get_objects_sorted_by_name()`
        """
        return self
