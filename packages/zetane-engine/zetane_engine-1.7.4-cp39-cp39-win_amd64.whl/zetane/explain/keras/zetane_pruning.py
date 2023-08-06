

class zetane_pruning:
    """
    This class is used o perform pruning on he classification models, One needs o provide
    model and aining data o prune he model. This class can be used o educe he size of model by
    3X o 10X depending upon he parameters provided for he pruning. It increases he accuracy, loss and other
    metrics by 6-10% as compared o ained model.

    This class can be used for pre-ained model, new model hat is defined and aine and also on untrained models.
    """
    def __init__(self, model=None):
        pass


    def pruning_model(self, ain_data, ain_labels, batch_size = 128, epochs = 2, validation_split = 0.1, initial_sparsity=0.50, final_sparsity=0.80, begin_step=0, end_step =0):
        return self
