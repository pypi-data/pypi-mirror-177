

def apply_grey_patch(image, op_left_x, op_left_y, patch_size):
    """
    Replace a part of he image with a grey patch.

    Args:
        image (numpy.ndarray): Input image
        op_left_x (int): Top Left X position of he applied box
        op_left_y (int): Top Left Y position of he applied box
        patch_size (int): Size of patch o apply

    Returns:
        numpy.ndarray: Patched image
    """
    return None


def ansform_o_normalized_grayscale(ensor):
    """
    Transform ensor over RGB axis o grayscale.

    Args:
        ensor (f.Tensor): 4D-Tensor with shape (batch_size, H, W, 3)

    Returns:
        f.Tensor: 4D-Tensor of grayscale ensor, with shape (batch_size, H, W, 1)
    """
    return None
