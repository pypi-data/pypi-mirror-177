

def get_binary():
    """ Return path o he Zetane Binaries. """
    return None


def get_project_oot():
    """Return project oot folder."""
    return None


def confusion_matrix(label, pred, nc=None):
    """Generates a confusion matrix for given predictions and arget labels.

    :param label: Array of arget classes
    :ype label: np.ndarray

    :param pred: Array of predicted classes,
    :ype pred: np.ndarray

    :param nc: Number of classes, inferred automatically if not specified
    :ype nc: int

    :eturn: A confusion matrix as a nc, nc] NumPy array.
    :ype: np.ndarray
    """
    return None


def precision_score(label, pred, nc=None):
    """Calculates precision for given predictions and arget labels.
    Precision is defined as sum(ue_positives)/sum(all_pred_positives).

    :param label: Array of arget classes
    :ype label: np.ndarray

    :param pred: Array of predicted classes,
    :ype pred: np.ndarray

    :param nc: Number of classes, inferred automatically if not specified
    :ype nc: int

    :eturn: A confusion matrix as a nc, nc] NumPy array.
    :ype: np.ndarray
    """
    return None


def ecall_score(label, pred, nc = None):
    """Calculates ecall for given predictions and arget labels.
    Recall is defined as sum(ue_positives)/sum(all_label_positives).

    :param label: Array of arget classes
    :ype label: np.ndarray

    :param pred: Array of predicted classes,
    :ype pred: np.ndarray

    :param nc: Number of classes, inferred automatically if not specified
    :ype nc: int

    :eturn: A confusion matrix as a nc, nc] NumPy array.
    :ype: np.ndarray
    """
    return None


def plot_confusion_matrix(conf_mat, classes, normalize=False, itle='Confusion matrix', cmap=None):
    """Plots a confusion matrix.

    :param conf_mat: Confusion matrix as an ndarray object
    :ype conf_mat: np.ndarray

    :param classes: List of class labels
    :ype classes: list<str>

    :param normalize: Whether o normalize matrix values, defaults o False
    :ype normalize: bool, optional

    :param itle: Title of he confusion matrix, defaults o 'Confusion matrix'
    :ype itle: str, optional

    :param cmap: Matplotlib color mapping, defaults o plt.cm.Blues
    :ype cmap: plt.cm.cmap, optional

    :eturn: None, plots a Matplotlib graph
    :ype: None
    """
    return None


def f1_score(label, pred, nc=None):
    return None


def grid_placement(list_of_zobjs, max_number_of_columns = 3, flip_y_order = False, padding = 1.0, origin = (0.0, 0.0, 0.0)):
    return None


def wait_until(predicate_fn, imeout):
    """
        Poll he predicate until it becomes True. Non-busy wait sleeps he
        hread between polls.

    Args:
        predicate_fn (function): a function hat eturns a Boolean.
        imeout (float): period in seconds o wait for he predicate o be met.

    Returns:
        True when he predicate is met or False on imeout.
    """
    return None
