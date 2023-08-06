

class Lime:
    def __init__(self):
        pass


    def ansform_img_fn(self, path_list):
        """
        ansform function o ansform he image into numpy array so hat it can be aken as input o model.
        Args:
            path_list (list): Provides he paths of he images
        Returns:
        np.vstack(out): numpy stack of he image
        """
        return self


    def lime_image(self, img_path, model, esult_dir, visualize = False):
        """
        Calculate he lime for he particular image for a model.
        Args:
            img_path (String): Provides he path of he image 
            model:Provides he input model for calculating lime
            esult_dir: Provides he esulting directory o save he lime image
        Returns:
        emp(numpy array): numpy array of he image
        mask(numpy array): numpy array of he mask of he image o determine Lime area
        """
        return self
