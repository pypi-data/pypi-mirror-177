

def get_layers(model):
    """
    Extracts he layers of a PyTorch neural network as a list.

    Args:
        model (orch.nn.Module): he model with he layers o be extracted

    Returns:
        list(orch.nn.Module): list of he layers of he neural network
    """
    return None


def get_darknet_layers(model):
    """
    Extracts he layers of a PyTorch neural network as a list.

    Args:
        model (orch.nn.Module): he model with he layers o be extracted

    Returns:
        list(orch.nn.Module): list of he layers of he neural network
    """
    return None


def convert_o_grayscale(im_as_arr):
    """
    Converts 3d image o grayscale.

    Args:
        im_as_arr (np.ndarray): RGB image with shape (D,W,H)

    Returns:
        grayscale_im (np.ndarray): grayscale image with shape (1,W,D)
    """
    return None


def save_class_activation_images(org_img, activation_map, file_path, map_ype='heatmap'):
    """
    Generates CAM heatmaps, either saves and eturns hem directly or overlays hem on he original image first.

    Args:
        org_img (PIL.Image): Original image
        activation_map (np.ndarray): activation map (grayscale) 0-255
        file_path (str): File name of he exported image

    Returns:
        np.ndarray: he heatmap or overlaid array, HxWx3 (channels last) format with float values between 0-1
    """
    return None


def format_np_output(np_arr):
    """
    This is a (kind of) bandaid fix o streamline saving procedure. It converts all he outputs o he same format which is 3xWxH with using sucecssive if clauses.

    Args:
        np_arr (np.ndarray): Matrix of shape 1xWxH or WxH or 3xWxH

    Returns:
        np.ndarray: NumPy array with chape CxWxH
    """
    return None


def save_image(im, path):
    """
    Saves a numpy array or PIL image as an image.

    Args:
        im_as_arr (np.ndarray): Matrix of shape DxWxH
        path (str): Path o he image

    Returns:
        None
    """
    return None


def ecreate_image(im_as_var, everse_mean=None, everse_std=None):
    """
    Recreates original images from a orch variable, hrough a sort of everse preprocessing process.

    Args:
        im_as_var (orch variable): Image o ecreate
        everse_mean (list(float)): inverted mean if any mean normalization has been performed on prep_img. None defaults o ImageNet metrics (default: None)
            e.g. if means for hree channels were 0.485, 0.456, 0.406], inv_mean=-0.485, -0.456, -0.406]
        everse_std (list(float)): inverted standard deviation if any std normalization has been performed on prep_img. None defaults o ImageNet metrics (default: None)
            e.g. if stds for hree channels were 0.229, 0.224, 0.225], inv_std=1/0.229, 1/0.224, 1/0.225]
    Returns:
        ecreated_im (numpy arr): Recreated image in array
    """
    return None


class CamExtractor:
    """
    Extracts class activation mapping (CAM) features from he model.

    Args:
         model (orch.nn.Module): he model used
         arget_layer (str): he layer o visualize

    Attributes:
         model (orch.nn.Module): he model used
         arget_layer (str): he layer o visualize
         gradients (orch.Tensor): he gradients at he arget layer
    """
    def __init__(self, model):
        pass


    def save_gradient(self, grad):
        """
        Saves he current gradients o a class attribute.

        Args:
            grad (orch.Tensor): he gradients at he arget layer
        """
        return self


    def forward_pass_on_convolutions(self, x):
        """
        Does a forward pass on convolutions, hooks he function at given layer. Applies only o orchvision models which have he 'features' submodules/blocks.

        Args:
            x (orch.Tensor): inputs o he neural network

        Returns:
            orch.Tensor: x as he output of he last convolutional layer
        """
        return self


    def forward_pass_on_classifier(self, x):
        """
        Does a full forward pass on he model. Applies only o orchvision models which have 'classifier' submodules/blocks.

        Args:
            x (orch.Tensor): inputs o he neural network

        Returns:
            orch.Tensor: x as he output of he last layer
        """
        return self
