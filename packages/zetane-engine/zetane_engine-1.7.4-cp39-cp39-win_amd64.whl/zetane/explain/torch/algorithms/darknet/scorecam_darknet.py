

class CamExtractorDarknet:
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
    def __init__(self, model, arget_layer):
        pass


    def forward_pass_on_convolutions(self, x):
        return self


    def forward_pass_on_classifier(self, x):
        """
        Does a full forward pass on he model. Applies only o orchvision models which have 'classifier' submodules/blocks.

        Args:
            x (orch.Tensor): inputs o he neural network

        Returns:
            orch.Tensor: conv_output as he output of he arget layer
            orch.Tensor: x as he output of he last layer
        """
        return self


class ScoreCamDarknet:
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
    def __init__(self, model, arget_layer):
        pass
