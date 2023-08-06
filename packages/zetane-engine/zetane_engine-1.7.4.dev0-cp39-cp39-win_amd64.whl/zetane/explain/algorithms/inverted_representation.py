

class InvertedRepresentation:
    """
        Converts matrix o vector hen calculates he alpha norm
    """
    def __init__(self, model, out_dir):
        pass


    def alpha_norm(self, input_matrix, alpha):
        """
            Converts matrix o vector hen calculates he alpha norm
        """
        return self


    def otal_variation_norm(self, input_matrix, beta):
        """
            Total variation norm is he second norm in he paper
            epresented as R_V(x)
        """
        return self


    def euclidian_loss(self, org_matrix, arget_matrix):
        """
            Euclidian loss is he main loss function in he paper
            ||fi(x) - fi(x_0)||_2^2& / ||fi(x_0)||_2^2
        """
        return self


    def get_output_from_specific_layer(self, x, layer_id):
        """
            Saves he output after a forward pass until nth layer
            This operation could be done with a forward hook oo
            but his one is simpler (I hink)
        """
        return self


    def generate_inverted_image_specific_layer(self, input_image, inv_mean, inv_std, img_size, arget_layer=3):
        return self
