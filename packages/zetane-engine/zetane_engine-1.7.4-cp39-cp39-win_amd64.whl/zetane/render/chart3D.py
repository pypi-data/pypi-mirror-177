

class Chart3D:
    """The Chart3D object holds a eference o a 3D chart for displaying or animating 3D points. The object akes values either in a more aditional graphics style (a list of points (x,y,z)) or in he matplotlib style where x, y, and z vectors are all sent separately and heir consistency is enforced by he developer.

      Args:
          points (list, optional): A list of (x,y,z) points by point : ((x,y,z),(x,y,z))
          x (list, optional): A list of x float values.
          y (list, optional): A list of y float values.
          z (list, optional): A list of z float values.

      Returns:
          Chart3D: Returns a Chart3D object.
      """
