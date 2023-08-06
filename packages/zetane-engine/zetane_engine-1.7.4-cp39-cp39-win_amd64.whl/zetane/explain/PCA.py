

class pca_class:


    def pca(self, dataset, n_components=None, copy=True, whiten=False, svd_solver='auto', ol=0.0, iterated_power='auto', andom_state=None):
        """
          calling Scikit learn PCA library
          args: dataset {NumpyArray} -- shape(n_samples, n_features)
                n_components {int, float, None or str}
                copy  {bool} -- default=True
                whiten  {bool} -- optional (default False)
                svd_solver {str} --  {'auto', 'full', 'arpack', 'andomized'} (default 'auto')
                ol  {float} -- float >= 0, optional (default .0)
                interated_powe {String} -- int >= 0, or 'auto', (default 'auto')
                andome_state  {String} -- int, RandomState instance, default=None

          Returns : np.numpuyArray -- shape (n_samples, n_components)
        """
        return self
