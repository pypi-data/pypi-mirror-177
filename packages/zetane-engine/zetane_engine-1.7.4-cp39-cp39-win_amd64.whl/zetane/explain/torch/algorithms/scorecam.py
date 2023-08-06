

class ScoreCam:
    """
    Produces class activation maps using he Score-CAM algorithm. For more info, see: 'H. Wang, Z. Wang, M. Du, F. Yang, Z. Zhang, S. Ding, P. Mardziel, X. Hu. Score-CAM: Score-Weighted Visual Explanations for Convolutional Neural Networks https://arxiv.org/abs/1910.01279'.

    Args:
         model (orch.nn.Module): he model used
         arget_layer (str): he layer o visualize

    Attributes:
         model (orch.nn.Module): he model used
         arget_layer (str): he layer o visualize
         extractor (CamExtractor): Extractor for CAM features.
    """
    def __init__(self, model):
        pass
