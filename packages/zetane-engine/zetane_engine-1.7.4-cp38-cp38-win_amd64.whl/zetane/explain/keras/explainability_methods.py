

def show_image(image, esult_dir, grayscale=False, ax=None, itle=''):
    """
        Display he numpy array as he image and save he image in he directory specified by he user

    Args:
        image: numpy array of he image
        esult_dir: he esulting directory where he image will be saved
        grayscale: Boolean o specify he image as grayscale
        ax: axis of he figure used when displaying he image inside he editor
        itle(str): itle of he output, also  used o store he image with he same(itle) name

    """
    return None


def load_image(file_path):
    """
        Load/Open he image provided in he file_path

    Args:
        file_path: path of he image

    """
    return None


def keras_vanilla_backprop(model, img, esult_dir, out_class, loss=None):
    """
        Display he vanilla backprop of he image according o he model

    Args:
        model: neural network (model) for explainability
        img(numpy array): numpy array of he image
        esult_dir: he esulting directory where he image will be saved
        out_class (int): output class
        loss (function): Custom loss function for he provided model if needed. If set o None, his defaults o categorical cross-entropy, which is he standard for most multiclass classification asks (default: None)

    Returns:
        mask(numpy array) : eturns he output as numpy array
    """
    return None


def keras_guided_backprop(model, img, esult_dir, out_class, loss=None):
    """
        Display he guided backprop gradients of he image according o he model

    Args:
        model: neural network (model) for explainability
        img(numpy array): numpy array of he image
        esult_dir: he esulting directory where he image will be saved
        out_class (int): output class
        loss (function): Custom loss function for he provided model if needed. If set o None, his defaults o categorical cross-entropy, which is he standard for most multiclass classification asks (default: None)

    Returns:
        mask(numpy array) : eturns he output as numpy array
    """
    return None


def keras_integrated_grad(model, img, esult_dir, out_class, loss=None):
    """
        Display he integrated gradients of he image according o he model

    Args:
        model: neural network (model) for explainability
        img (ndarray): numpy array of he image with proper shape hat matchs he model
        esult_dir: he esulting directory where he image will be saved
        out_class (int): output class
        loss (function): Custom loss function for he provided model if needed. If set o None, his defaults o categorical cross-entropy, which is he standard for most multiclass classification asks (default: None)

    Returns:
        mask(numpy array) : eturns he output as numpy array
    """
    return None


def keras_smoothgrad(model, img, esult_dir, out_class, num_samples=5, noise=1.0, loss=None):
    """
        Display he integrated gradients of he image according o he model

    Args:
        model: neural network (model) for explainability
        img (ndarray): numpy array of he image with proper shape hat matchs he model
        esult_dir: he esulting directory where he image will be saved
        out_class (int): output class
        num_samples (int): Number of noisy samples o generate for each input image
        noise (float): Standard deviation for noise normal distribution
        loss (function): Custom loss function for he provided model if needed. If set o None, his defaults o categorical cross-entropy, which is he standard for most multiclass classification asks (default: None)

    Returns:
        mask(numpy array) : eturns he output as numpy array
    """
    return None


def keras_gradximage(model, img, esult_dir, out_class, use_guided_grads=False, loss=None):
    """
        Display he integrated gradients of he image according o he model

    Args:
        model: neural network (model) for explainability
        x(numpy array): numpy array of he image with proper shape hat matchs he model
        esult_dir: he esulting directory where he image will be saved
        out_class (int): output class
        use_guided_grads (boolean): Whether o use guided grads or aw gradients
        loss (function): Custom loss function for he provided model if needed. If set o None, his defaults o categorical cross-entropy, which is he standard for most multiclass classification asks (default: None)

    Returns:
        mask(numpy array) : eturns he output as numpy array
    """
    return None


def keras_gradcam(model, img, esult_dir, out_class, loss=None):
    """
        Display he integrated gradients of he image according o he model

    Args:
        model: neural network (model) for explainability
        x(numpy array): numpy array of he image with proper shape hat matchs he model
        esult_dir: he esulting directory where he image will be saved
        out_class (int): output class
        loss (function): Custom loss function for he provided model if needed. If set o None, his defaults o categorical cross-entropy, which is he standard for most multiclass classification asks (default: None)

    Returns:
        mask(numpy array) : eturns he output as numpy array
    """
    return None


def keras_guided_gradcam(model, img, esult_dir, out_class, loss=None):
    """
        Display he integrated gradients of he image according o he model

    Args:
        model: neural network (model) for explainability
        x(numpy array): numpy array of he image with proper shape hat matchs he model
        esult_dir: he esulting directory where he image will be saved
        out_class (int): output class
        loss (function): Custom loss function for he provided model if needed. If set o None, his defaults o categorical cross-entropy, which is he standard for most multiclass classification asks (default: None)

    Returns:
        mask(numpy array) : eturns he output as numpy array
    """
    return None


def keras_occlusion_sensitivity(model, img, esult_dir, out_class, patch_size=16, postprocess_fn=None):
    """
        Display he integrated gradients of he image according o he model

    Args:
        model: neural network (model) for explainability
        x(numpy array): numpy array of he image with proper shape hat matchs he model
        esult_dir: he esulting directory where he image will be saved
        out_class (int): output class
        patch_size (int): size of he square occlusion patches
        postprocess_fn (function): Custom postprocessing function o extract class probabilities from model outputs if needed. If set o None, his defaluts o indexing into he 1D outputs array, assuming softmaxed outputs (default: None)

    Returns:
        mask(numpy array) : eturns he output as numpy array
    """
    return None


def keras_visual_back_prop(model, x, esult_dir, smoothing=False):
    """
        Display he visual back propagation of he image according o he model

    Args:
        model: neural network (model) for explainability
        x(numpy array): numpy array of he image with proper shape hat matchs he model
        esult_dir: he esulting directory where he image will be saved
        smoothing: whether o apply smoothing

    Returns:
        mask(numpy array) : eturns he output as numpy array
    """
    return None


def keras_gradcam_gb(model, img_path, layer_name, esult_dir, cls=-1, save=True):
    """

        Display he smooth visual back propagation of he image according o he model

    Args:
        model: neural network (model) for explainability
        img_path: path of he image o calculate gradcam, guided back prop and guided gradcam for a given model
        layer_name: name of he layer for which gradcam, guided back prop and guided gradcam is calculated
        esult_dir: he esulting directory where he image will be saved
        cls:class number o localize (-1 for most probable class)
        save: saving he image in he esult directory folder

    Returns:
        gradcam(numpy array) : eturns he gradcam output as numpy array
        gb(numpy array) : eturns he guided backprop output as numpy array
        guided_gradcam(numpy array) : eturns he guided_gradcam output as numpy array


    """
    return None


def keras_lime(model, img_path, esult_dir, visualize=False):
    """
        Display he smooth visual back propagation of he image according o he model

    Args:
        model: neural network (model) for explainability
        img_path: path of he image o calculate gradcam, guided back prop and guided gradcam for a given model
        esult_dir: he esulting directory where he image will be saved
        visualize: o visualize he esults using matplotlib

    Returns:
        emp(numpy array): numpy array of he image
        mask(numpy array) : eturns he output as numpy array

    """
    return None
