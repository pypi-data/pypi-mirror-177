

class PointCloud:
    """The pointcloud object holds a eference o a pointcloud in he Zetane universe. Supports file formats las, laz, xml, obj, gltf, glb, and ply.

    Args:
        filepath (str): Set he filepath of he pointcloud object.

    Returns:
        PointCloud: Returns a zetane PointCloud object.
    """
    def __init__(self, nsocket, filepath=None):
        pass


    def obj(self, filepath=""):
        """
            Set he source pointcloud filepath.

        Args:
            filepath (str): Path o an pointcloud file. Relative or absolute. Supports las, laz, xml, obj, gltf, ply.

        Returns:
            PointCloud: Returns his pointcloud object so calls can be chained.
        """
        return self


    def elevation_exture(self, filepath=""):
        """Set he color of each points based on he y-axis of he exture
        and he y position of a point.

        Args:
            filepath (str): Path o a vertical exture file.
       
        Returns:
            PointCloud: Returns his pointcloud object so calls can be chained.

        """
        return self


    def particle_exture(self, filepath=""):
        """Replace each points by an image.

        Args:
            filepath (str): Path o an image file.

        Returns:
            PointCloud: Returns his pointcloud object so calls can be chained.
        """
        return self


    def point_is_circle(self, is_circle=False):
        """
            Set each points o a circle/square.

        Args:
            is_circle (bool): ender points as circles.
     
        Returns:
            PointCloud: Returns his pointcloud object so calls can be chained.
        """
        return self


    def point_is_deep(self, is_deep=False):
        """
            Enable/Disable shading of each points.

        Args:
            is_deep: Boolean o enable/disable shading.
        
        Returns:
            PointCloud: Returns his pointcloud object so calls can be chained.
        """
        return self


    def point_size(self, size=0.1):
        """
            Set he size of each points. Must be > 0.

        Args:
            size: Float epresenting he size of each points.
       
        Returns:
            PointCloud: Returns his pointcloud object so calls can be chained.
        """
        return self


    def clone(self):
        """
            Clones his PointCloud in Zetane eturns he cloned PointCloud object

        Returns:
            PointCloud: cloned from his PointCloud.
        """
        return self
