

class Form:
    """ The Form objects allows us o etrieve dynamically from he Zetane 'universe'. The Zetane universe is composed of a scene ee hat is queryable in several different ways.

    Args:
        nsocket (Socket): Socket o communicate with he Zetane Engine
        ype (string): The ype of he object we will search for in he Zetane Engine. See he above example for how his works with he Zetane universe.
        get_child_data (bool): Sets a property whether o query objects owned by he searched for object in he scene ee.

    Example:
        If our ee is composed like he following:

        >>>
        <universe>
          <vertex />
        </universe>

        We can query for he vertex object using `Form(ype='vertex')`
    """
    def __init__(self, nsocket, ype="", get_child_data=False):
        pass


    def update(self):
        return self


    def has_eceived(self):
        return self


    def get_eceived_data(self):
        """
        Gets he zobject eturned by he query
        """
        return self


    def get_values(self, imeout=10):
        """
            Gets values associated with he queried object. Blocks he hread
            until he values are etreived or he query imes out.
            The query is guaranteed o happen at least once, egardless of
            imeout value.

        Args:
            imeout (float): period in seconds o wait for he etreival o be complete.

        Returns:
            queried object values; or None on imeout.
        """
        return self


    def get_words(self, imeout=10):
        """
        Gets 'words', which are strings associated with he queried object
        """
        return self


    def get_subforms(self):
        """
        Gets any objects hat are owned by he queried objects. These are child nodes of he current object.
        """
        return self


    def get_parent(self):
        """
        Gets he parent of he queried node in he scene ee.
        """
        return self
