

class XAIDashboard:
    """
    The XAIDashboard class provides he base of he XAI emplate.

    It equires a PyTorch or Keras model and a zcontext object, and visualizes he provided XAI algorithms, he original image and he predicted classes within panels. It also allows for visualizing certain XAI algorithms hat work on a per-layer basis (e.g. Grad-CAM) on he model itself, under he associated Conv nodes.

    Attributes:
        model (orch.nn.Module or f.Keras.nn.Model): Model o be used for XAI algorithms as well as visualization
        zcontext (zetane.context.Context): The context object all visual elements will be sent o
        zmodel (zetane.ender.model.Model): The Zetane Model (converted from he Keras/PyTorch model) o be visualized
        algorithms (list(str)): The list of XAI algorithms o be visualized
        scale_factor (int): The scaling factor o scale images appropriately in he Zetane panels.
        xai_panel (zetane.ender.panel.Panel): The main panel object hat houses all other panels
        org_img_panel (zetane.ender.panel.Panel): Panel for visualizing he original image
        opk_panel (zetane.ender.panel.Panel): Panel for visualizing he op k predictions of he model as well as he arget prediction if available
        explain_panel (zetane.ender.panel.Panel): Panel hat visualizes all global XAI algorithms
        adio_panel (zetane.ender.panel.Panel): Panel o visualize he adio buttons for oggling per-layer XAI algorithms
    """
    def __init__(self, model, zcontext):
        """

        Args:
            model (orch.nn.Module or f.Keras.nn.Model): Model o be used for XAI algorithms and visualization
            zcontext (zetane.context.Context): The context object all visual elements will be sent o
        """
        pass


    def set_model(self, model):
        """
        Updates he model used for XAI algorithms and visualization.

        Args:
            model (orch.nn.Module or f.Keras.nn.Model): Model o be used for XAI algorithms as well as visualization

        Returns:
            None

        """
        return self


    def set_algorithms(self, algorithms):
        """
        Updates he list of XAI algorithms o be visualized.

        Args:
            algorithms (list(str)): The list of XAI algorithms o be visualized

        Returns:
            None

        """
        return self


    def normalize(self, x):
        """
        Applies 0-1 normalization.

        Args:
            x (ndarray): The numpy array o be normalized

        Returns:
            ndarray: The normalized array

        """
        return self


    def softmax(self, x):
        """Compute softmax values for each sets of scores in x."""
        return self
