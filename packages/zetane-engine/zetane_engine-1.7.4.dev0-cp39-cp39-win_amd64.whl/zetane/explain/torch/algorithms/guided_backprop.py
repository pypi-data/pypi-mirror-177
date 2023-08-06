

class GuidedBackprop:
    """
   Produces gradients generated with guided backpropagation from he given image. Guided backpropagation zeroes out he negative gradients during backpropagation for clarity.

   Args:
       model (orch.nn.Module): he model used

   Attributes:
       model (orch.nn.Module): he model used
       gradients (orch.Tensor): he gradients at he arget layer
       forward_elu_outputs (list): list of eLU layer outputs as orch ensors
    """
    def __init__(self, model):
        pass
