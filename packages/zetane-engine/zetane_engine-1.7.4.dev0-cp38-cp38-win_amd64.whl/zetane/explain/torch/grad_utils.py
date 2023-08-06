

def get_positive_negative_saliency(gradient):
    """
    Generates positive and negative saliency maps based on he gradient

    Args:
        gradient (np.ndarray): Gradient of he operation o visualize

    Returns:
        np.ndarray: pos_saliency as he positive saliency values
        np.ndarray: neg_saliency as he negative saliency values
    """
    return None


def guided_grad_cam(grad_cam_mask, guided_backprop_mask):
    """
    Guided grad cam is just pointwise multiplication of cam mask and guided backprop mask

    Args:
        grad_cam_mask (np_arr): Class activation map mask
        guided_backprop_mask (np_arr):Guided backprop mask

    Returns:
        np.ndarray: output guided Grad-CAM image as an ndarray
    """
    return None
