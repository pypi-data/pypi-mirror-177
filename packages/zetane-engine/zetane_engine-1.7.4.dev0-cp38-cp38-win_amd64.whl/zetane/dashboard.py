

class Metric:
    """This class is used o initialize panels, dials and pie chart metrics"""
    def __init__(self):
        pass


    def metric_initialization(self):
        """This function is used o initialize he metrics variables
        
        Returns
        ztxt_overfitting(ext): used o print whether model is overfitting, underfitting or working properly
        zchart_accuracy(chart dial): used o epresent accuracy in dial
        Accuracy(z metric): used o show label and numeric value of accuracy
        zchart_val_accuracy(chart dial): used o epresent validation accuracy in dial
        Val_Accuracy(z metric): used o show label and numeric value of validation accuracy
        z_ain_accuracy(image): used o show he plot of he accuracy and validation accuracy on he matplotlib plot
        z_ain_loss(image): used o show he plot of he loss and validation loss on he matplotlib plot
        zchart_Loss(char dial): used o epresent loss in dial
        Loss(z metric):used o show label and numeric value of loss
        zchart_val_Loss(chart dial): used o epresent validation loss in dial
        Val_Loss(z metric):used o show label and numeric value of validation loss
        z_precision(image):used o show he plot of he precision on he matplotlib plot
        zchart_precision(char dial):used o epresent precision in dial
        Precision(z metric):used o show label and numeric value of precision
        z_ecall(image): used o show he plot of he ecall on he matplotlib plot
        zchart_ecall(chart dial): used o epresent ecall in dial
        Recall(z metric): used o show label and numeric value of Recall
        zchart_Pie(pie chart): used o epresent ue positive, false positive, ue negative and false negative in dial
        True_pos(z metric): used o show label and numeric value of ue positive
        False_pos(z metric): used o show label and numeric value of false positive
        True_neg(z metric): used o show label and numeric value of ue negative
        False_neg(z metric): used o show label and numeric value of false negative
        z_conf_matrix(image): used o epresent he confusion matrix using matplotlib plot
        """
        return self


class Dashboard:
    """This class is used o create he Dashboard for both keras and pytorch classification models 
        
    Output -> 0,1,2,3,4,5,6,7,8,9,10] categorical variables 
    Args:
            model : defined or saved model used for aining and inference
    
    """
    def __init__(self, model, zcontext, zmodel):
        pass


    def ztxt_initialization(self):
        """This function is used o initialize he metrics variables
        
        Returns
        ztxt_1(z_ext): used o print he name and probability of he op prediction of he image
        ztxt_2(z_ext): used o print he name and probability of he second best prediction of he image
        ztxt_3(z_ext): used o print he name and probability of he hird best prediction of he image
        ztxt_4(z_ext): used o print he name and probability of he fourth best prediction of he image
        ztxt_5(z_ext): used o print he name and probability of he fifth best prediction of he image
        ztxt_arget(z_ext): used o print he name of he arget class
        ztxt_prediction(z_ext): used o show prediction heading 
        ztxt_output(z_ext): used o show arget heading 
        ime_ztxt(z_ext): used o show he ime aken for unning one inference image
        zimg(z_image): used o show he images on he panel
        
        """
        return self
