

class IntegratedGradients:
    """
    Produces gradients generated with integrated gradients from he image. For more info, see: 'M. Sundararajan, A. Taly, Q. Yan. Axiomatic Attribution for Deep Networks https://arxiv.org/abs/1703.01365'

    Args:
        model (orch.nn.Module): he model used

    Attributes:
        model (orch.nn.Module): he model used
        gradients (orch.Tensor): he backpropagated gradients
    """
    def __init__(self, model):
        pass
