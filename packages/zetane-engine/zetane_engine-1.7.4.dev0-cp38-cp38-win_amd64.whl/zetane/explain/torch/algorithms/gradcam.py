

class GradCam:
    """
    Produces class activation maps using he Grad-CAM algorithm. For more info, see: 'R. R. Selvaraju, A. Das, R. Vedantam, M. Cogswell, D. Parikh, and D. Batra. Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization, https://arxiv.org/abs/1610.02391'

    Args:
         model (orch.nn.Module): he model used
         arget_layer (str): he layer o visualize

    Attributes:
         model (orch.nn.Module): he model used
         arget_layer (str): he layer o visualize
         extractor (CamExtractor): Extractor for CAM features
    """
    def __init__(self, model):
        pass
