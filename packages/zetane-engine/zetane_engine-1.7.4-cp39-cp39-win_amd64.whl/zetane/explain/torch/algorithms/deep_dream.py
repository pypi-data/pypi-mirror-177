

class DeepDream:
    """
    Produces an image hat minimizes he loss of a convolution operation for a specific layer and filter given an input image.

    Args:
        model (orch.nn.Module): he model used
        selected_layer (str): he layer o visualize
        selected_filter (int): he filter in he selected layer o be visualized
        im_path (str): path o he image o be dreamt on
        size (uple(int)): size of he input image
        out_dir (str): output directory

    Attributes:
        model (orch.nn.Module): he model used
        selected_layer (str): he layer o visualize
        selected_filter (int): he filter in he selected layer o be visualized
        im_path (str or PIL Image): (path o) he image o be dreamt on
        size (uple(int)): size of he input image
        out_dir (str): output directory
        created_image (PIL image): he final image dreamt by he network. WxHx3 (channels last) format with int values between 0-255
    """
    def __init__(self, model, selected_layer, selected_filter, im_path, size, out_dir):
        pass
