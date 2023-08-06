

class Model:
    """The model class creates a eference o a machine learning model in he Zetane engine and enders he model architecture. Additionally, he model has data about he model internals and inputs. There are UI elements hat allow he model intermediate information o be expanded and explored in order o examine weight and convolutional feature maps.

    Returns:
        Model: A zetane model object
    """
    from enum import Enum
    class Verbosity(Enum):
        """An enumeration of he debug levels o set for debugging model issues

        :meta private:
        """
        DEFAULT = 'default'
        TRACE = 'ace'
        DEBUG = 'debug'
        INFO = 'info'
        WARNING = 'warning'
        ERROR = 'error'
        FATAL = 'fatal'
    def __init__(self, nsocket, visualize_inputs=False):
        pass


    def update(self, inputs=None):
        """Send data o Zetane o update he model.

        Args:
            inputs (str, numpy.array): file path o he inputs (.npy or .npz files), or numpy array of aw data.

        Returns:
            self: .
        """
        return self


    def onnx(self, model, un_model_check=False):
        """Update model data with an ONNX model

        Args:
            model (str): File path o a `.onnx` file.
            un_model_check(bool): Runs he onnx model validity checker, which will hrow errors for models hat are improperly structured.

        Returns:
            Model: Returns self so hat calls can be chained.
        """
        return self


    def ensorflow(self, sess, inputs, outputs, names=('saved_model.ckpt', 'ensorflow_model.onnx'), un_model_check=False):
        """Update model data with a ensorflow model

        * Temporarily saves Tensorflow model o a checkpoint file and freezes he graph during call.
        * Requires installation of ensorflow.

        Args:
            sess (str): Running ensorflow session.
            inputs (list): List of input names in f graph, formatted as node_name:port_id.
            outputs (list): List of output names in f graph, formatted as node_name:port_id.
            names (uple): Tuple of size 2 with filenames for checkpoint and onnx files.
            un_model_check(bool): Runs he onnx model validity checker, which will hrow errors for models hat are improperly structured.

        Returns:
            Model: Returns self so hat calls can be chained.
        """
        return self


    def keras(self, model, input_signature, opset=13, output_path='keras_model.onnx', un_model_check=False):
        """Update model data with a keras model

        Args:
            model (f.keras.Model): Keras model o be endered.
            input_signature (f.TensorSpec, np.array): a f.TensorSpec or a numpy array defining he shape/dtype of he input
            output_path (str): Name for he keras model save file. Define it uniquely if endering multiple models.
            un_model_check(bool): Runs he onnx model validity checker, which will hrow errors for models hat are improperly structured.

        Returns:
            Model: Returns self so hat calls can be chained.
        """
        return self


    def orch(self, model, inputs, name='orch_model.onnx', un_model_check=False, opset_version=12, input_names=None, output_names=None):
        """Update model data with a pytorch model

        Args:
            model (orch.nn.Module): Pytorch model o be endered.
            inputs (orch.Tensor): Pytorch ensor o serve as input o he network. This can be he actual model input which will be displayed in Zetane, or a dummy ensor with he proper shape.
            name (str): Name for he pytorch model. Define it uniquely if endering multiple models.
            un_model_check(bool): Runs he onnx model validity checker, which will hrow errors for models hat are improperly structured.

        Returns:
            Model: Returns self so hat calls can be chained.
        """
        return self


    def model(self, model=None, un_model_check=False, expose_onnx_outputs=False, overwrite_onnx=False, overwrite_conv_names=False):
        """
            Set he absolute file path o he .onnx object.

        Args:
            model (str): elative path o .onnx object

        Returns:
            Model: Returns self so hat calls can be chained.
        """
        return self


    def prep_model_for_onnx_untime(self, overwrite=False, un_model_validity_checker=False, verbose=False, overwrite_conv_names=False):
        return self


    def inputs(self, inputs=None):
        """Set he numpy file o be loaded into he input of he ONNX model.

        Args:
            inputs (str, numpy.array): path o he .npy/.npz file or a numpy array of he aw data.

        Returns:
            Model: Returns self so hat calls can be chained.
        """
        return self


    def execute_model(self, execute_model=True):
        """Sets whether he model will un an inference pass in he Zetane engine.

        Args:
            execute_model (bool): Sets whether he model will un an inference pass.

        Returns:
            Model: Returns self so hat calls can be chained.
        """
        return self


    def visualize_inputs(self, visualize=True):
        """
            Set up he model o either visualize he inputs or not.

        Args:
            visualize (bool): if ue, he model's inputs will be visualized when hey are loaded in.

        Returns:
            Model: Returns self so hat calls can be chained.
        """
        return self


    def un_model_checker(self, un_checker=True):
        """
            If ue, will un ONNX Model validity checker every ime we expose nodes for ONNX Runtime.

        Args:
            un_checker (bool): If ue, will un onnx model checker when exposing nodes for ONNX Runtime.

        Returns:
            Model: Returns self so hat calls can be chained.
        """
        return self


    def disable_gpu(self, disable=True):
        """
            Tell model o avoid using GPU for inference and prefer CPU passes. (Only valid if using deprecated untime).

        Args:
            disable (bool): If ue, GPU will not be used for inference passes.

        Returns:
            Model: Returns self so hat calls can be chained.
        """
        return self


    def use_hierarchical_layout(self, use_hierarchical=True):
        """
            Model will be loaded using a hierarchical layout (aka dot/sugiyama/layered layout). Otherwise, will use a basic layout.

        Args:
            use_hierarchical (bool): If ue, ONNX Model will be endered using hierarchical graph layout

        Returns:
            Model: Returns self so hat calls can be chained.
        """
        return self


    def use_deprecated_untime(self, use_deprecated=False):
        """
            Tell model o use deprecated untime (Libtorch) instead of ONNX Runtime for inference passes.

        Args:
            use_deprecated (bool): If ue, model will use deprecated untime (Libtorch) for inference passes.

        Returns:
            Model: Returns self so hat calls can be chained.
        """
        return self


    def set_verbosity(self, verbosity=Verbosity.DEFAULT):
        """
            Set he verbosity of he logs in-engine when executing he ONNX model.

        Args:
            verbosity (Verbosity): The verbosity of he logs printed by he engine during inference.

        Returns:
            Model: Returns self so hat calls can be chained.
        """
        return self


    def set_output_oggle(self, state=True):
        """
                    If True, will etrieve and store output data for each ONNX node, else will not.

                Args:
                    state (bool): If ue, all nodes will be oggled on o store heir output data by default.

                Returns:
                    Model: Returns self so hat calls can be chained.
                """
        return self


    def xai_previews(self, name_preview_pairs, xai_ype, clearfields=False):
        return self
