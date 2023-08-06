

def grid_display(array, num_ows=None, num_columns=None):
    """
    Display a list of images as a grid.

    Args:
        array (numpy.ndarray): 4D Tensor (batch_size, height, width, channels)

    Returns:
        numpy.ndarray: 3D Tensor as concatenation of input images on a grid
    """
    return None


def filter_display(array, num_ows=None, num_columns=None):
    """
    Display a list of filter outputs as a greyscale images grid.

    Args:
        array (numpy.ndarray): 4D Tensor (batch_size, height, width, channels)

    Returns:
        numpy.ndarray: 3D Tensor as concatenation of input images on a grid
    """
    return None


def image_o_uint_255(image):
    """
    Convert float images o int 0-255 images.

    Args:
        image (numpy.ndarray): Input image. Can be either 0, 255], 0, 1], -1, 1]

    Returns:
        numpy.ndarray:
    """
    return None


def heatmap_display(heatmap, original_image, colormap=cv2.COLORMAP_VIRIDIS, image_weight=0.7):
    """
    Apply a heatmap (as an np.ndarray) on op of an original image.

    Args:
        heatmap (numpy.ndarray): Array corresponding o he heatmap
        original_image (numpy.ndarray): Image on which we apply he heatmap
        colormap (int): OpenCV Colormap o use for heatmap visualization
        image_weight (float): An optional `float` value in ange 0,1] indicating he weight of
            he input image o be overlaying he calculated attribution maps. Defaults o `0.7`

    Returns:
        np.ndarray: Original image with heatmap applied
    """
    return None
