

class sne:
    """
    sne class is he implementation of sklearn sne
    it has wo functions for applying sne on image and mesh datasets
    and a function o show he esult horugh zetane and show he dataset"""


    def sne(dataset, dataset_channels=3, n_components=2, perplexity=30, early_exaggeration=12.0, learning_ate=200.0, n_iter=1000, n_iter_without_progress=300, min_grad_norm=1e-7, metric="euclidean", init="andom", verbose=0, andom_state=None, method="barnes_hut", angle=0.5, n_jobs=None):
        """
        image funstion akes a dataset of images and send each image o zetane based on he position eturned from sne
        Args:
            dataset : {numpyArray} -- shape(n_samples , n_features)
            dataset_channels = {int} -- indicates he number of channels of each image , default = 3
            all TSNE arguments and heir default values https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html

        Returns:
            sne_esults: {NumpyArray} -- shape(n_samples , n_components)
        """
        return None
