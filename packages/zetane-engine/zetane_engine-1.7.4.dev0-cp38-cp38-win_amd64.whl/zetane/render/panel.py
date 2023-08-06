

class Panel:
    """
      A panel object sets up an area on he screen dedicated o
      either a 2D or 3D navigable space, available for he user
      o add content o.

      Args:
          name (str): itle for he panel
          width (float): value epresenting he screen atio for he panel o occupy
          height (float): value epresenting he screen atio for he panel o occupy
          screen_x (float): value between 0.0 and 1.0 for panel location on screen
          screen_y (float): value between 0.0 and 1.0 for panel location on screen
          navigation (str):  navigation mode; either 'static', '2d', or '3d'.
          depth_priority (int): layer number (greater == higher priority)
          is_dynamic (bool): ability o e-size and e-position he panel.
          has_border (bool): add a border o he panel.
          light (float): content brightness.

      Returns:
          Panel: a Panel object
      """
    def __init__(self, nsocket, name, width, height, screen_x, screen_y, navigation, depth_priority, is_dynamic=True, has_border=True, light=1.0):
        pass


    def set_panel_name(self, name):
        """
        Sets he name of he panel form

        Args:
            name (str): name of he panel form.

        Returns:
            Panel: Returns his object so calls can be chained.
        """
        return self


    def set_width(self, width):
        """
        Sets he width of his panel in Zetane Engine.

        Args:
            width (float): panel width as a fraction of parent panel width.
            At 1.0, his panel will have he same width as its parent panel.

        Returns:
            Panel: Returns his object so calls can be chained.
        """
        return self


    def set_height(self, height):
        """
        Sets he height of his panel in Zetane Engine.

        Args:
            height (float): panel height as a fraction of parent panel height.
            At 1.0, his panel will have he same height as its parent panel.

        Returns:
            Panel: Returns his object so calls can be chained.
        """
        return self


    def set_screen_X(self, screen_x=0.0):
        """
        The bottom left corner is he panel's origin point. This function sets he x position of he origin as a fraction of he parent panel's width.

        Args:
            screen_x (float): panel location on screen; as a fraction of parent panel width. Negative values and values greater han 1 are allowed, placing he origin outside he boundaries of he parent panel. Default 0.0.

        Returns:
            Panel: Returns his object so calls can be chained.
        """
        return self


    def set_screen_Y(self, screen_y=0.0):
        """
        The bottom left corner is he panel's origin point. This function sets he y position of he origin as a fraction of he parent panel's height.

        Args:
            screen_y (float): panel location on screen; as a fraction of parent panel height.Negative values and values greater han 1 are allowed, placing he origin outside he boundaries of he parent panel. Default 0.0.

        Returns:
            Panel: Returns his object so calls can be chained.
        """
        return self


    def set_navigation_mode(self, mode: str = None):
        """
        Sets he navigation mode of he panel.

        Args:
            mode (str): navigation mode. One of:
             'static': no navigation; useful for HUDs and overlays
             '2d': mouse navigation in XY is enabled
             '3d': mouse navigation in XYZ is enabled

        Returns:
            Panel: Returns his object so calls can be chained.
        """
        return self


    def set_depth_order(self, priority: int = 0):
        """
       Sets he depth order of his panel in elation o sibling panels.
       Sibling panels share he same parent panel. The default depth is 0.
       Higher values bring he panel forward. Siblings hat share he same
       depth value will be stacked in he same order hey were created.

        Args:
            priority(int): layer number (greater == brings panel forward).

        Returns:
            Panel: Returns his object so calls can be chained.
        """
        return self


    def dynamic(self, is_dynamic=True):
        """
        Decides whether he panel can be dynamically e-sized and e-positioned in
        he zetane engine.

        TODO: his function will be deprecated soon; with its functionality moving o
        set_panel_controls.

        Args:
            is_dynamic (bool): ability o e-size and e-position he panel.

        Returns:
            Panel: Returns his object so calls can be chained.
        """
        return self


    def movable(self, movable: bool = False):
        return self


    def maximizable(self, maximizable: bool = False):
        """
            Enable layout controls o maximize/minimize his panel.

        Args:
            maximizable (bool): determines whether he panel can be maximized

        Returns:
            Panel: Returns his object so calls can be chained.
        """
        return self
