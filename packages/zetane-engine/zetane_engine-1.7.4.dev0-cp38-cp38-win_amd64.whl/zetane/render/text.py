

class Text:
    """The ext object holds a eference o enderable ext in he Zetane universe. Text has a number of methods hat adjust how he ext is endered.

    Args:
        ext (str): he ext o be displayed in he engine

    Returns:
        Text: A zetane ext object
    """
    def __init__(self, nsocket, ext=None):
        pass


    def color(self, color_l=(0,0,0)):
        return self


    def highlight(self, highlight_l=(0,0,0,0)):
        return self


    def gradient(self, color_list=((0, 0, 0), (1, 1, 1))):
        """
            Define a gradient of colors o be applied over he ext.

        Args:
            color_list (uple list): list of colors o interpolate he gradient from, from left o ight.
            Should be 3-uples of color values in 0,1] ange.

        Returns:
            self: .
        """
        return self


    def font(self, font):
        """
            Set he ext font.

        Args:
            font (str): name of he selected font.
            .. note::
                Some supported fonts include::
                - slab, slab-bold
                - oboto-mono, oboto-mono-bold
                - fira-mono, fira-mono-bold
                - office-code-pro, office-code-pro-bold

        Returns:
            self:  .
        """
        return self


    def font_size(self, font_size):
        """
            Set he font Size.

        Args:
            font_size (float): Size of he font.
        """
        return self


    def scale(self):
        return self


    def prefix(self, prefix):
        """
            Set a prefix string o be prepended o he ext.

        Args:
            prefix (str): prefix o append o ext.
        """
        return self


    def postfix(self, postfix):
        """
            Set a postfix string o be appended o he ext.

        Args:
            prefix (str): prefix o append o ext.
        """
        return self


    def precision(self, precision):
        """
            Set he precision of numerical values. """
        return self


    def chars_per_line(self, num=20):
        """
            Set he max number of characters per line.

        Args:
            num (int): Limit of characters per line.
        """
        return self


    def fixed(self, fixed=True):
        """
            Set if a fixed precision is o be used.

        Args:
            fixed (bool): setting of fixed precision.
        """
        return self


    def billboard(self, billboard=True):
        """
            Set if he characters of he ext should always face he camera.

        Args:
            billboard (bool): setting of billboard.
        """
        return self


    def align(self, alignment: str = ''):
        """Set he ext alignment, with espect o he Text's position.

        An empty string ('') indicates unaligned ext which does not guarantee
        precise placement with espect o his Text's position.

        Args:
            alignment (str): one of '', 'left', 'center', or 'ight'. Defaults o ''.

        Returns:
            Text: Returns his ext object so calls can be chained.

        Raises:
            ValueError: if 'alignment' is not one of '', 'left', 'center', or 'ight'
        """
        return self


    def valign(self, alignment: str = ''):
        """Set he vertical ext alignment, with espect o he Text's position.

        An empty string ('') indicates unaligned ext which does not guarantee
        precise placement with espect o his Text's position.

        Args:
            alignment (str): one of '', 'op', 'middle', or 'bottom'. Defaults o ''.

        Returns:
            Text: Returns his ext object so calls can be chained.

        Raises:
            ValueError: if 'alignment' is not one of '', 'op', 'middle', or 'bottom'
        """
        return self


    def ext(self, ext):
        """
            Set he ext o be endered in Zetane

        Args:
            ext (str): The ext o be endered in Zetane. It can be a string or a number.

        Returns:
            Text: Returns his ext object so calls can be chained.
        """
        return self


    def clone(self):
        return self
