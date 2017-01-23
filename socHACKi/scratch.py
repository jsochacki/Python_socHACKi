from socHACKi.socHACKiUtilityPackage import AttrDict

class MovingObject(object):
    """
    MovingObject should be assigned to each moving object that is detected
    It will have the following attributes

    self.coordinates.top.left.x = self.coordinates.left.top.x
    self.coordinates.top.left.y = self.coordinates.left.top.y
    self.coordinates.top.right.x = self.coordinates.right.top.x
    self.coordinates.top.right.y = self.coordinates.right.top.y
    self.coordinates.bottom.left.x = self.coordinates.left.bottom.x
    self.coordinates.bottom.left.y = self.coordinates.left.bottom.y
    self.coordinates.bottom.right.x = self.coordinates.right.bottom.x
    self.coordinates.bottom.right.y = self.coordinates.right.bottom.y
    self.coordinates.left.top.x = self.coordinates.top.left.x
    self.coordinates.left.top.y = self.coordinates.top.left.y
    self.coordinates.left.bottom.x = self.coordinates.bottom.left.x
    self.coordinates.left.bottom.y = self.coordinates.bottom.left.y
    self.coordinates.right.top.x = self.coordinates.top.right.x
    self.coordinates.right.top.y = self.coordinates.top.right.y
    self.coordinates.right.bottom.x = self.coordinates.bottom.right.x
    self.coordinates.right.bottom.y = self.coordinates.bottom.right.y

    Half of the attributes are derived from the other attributes

    In order to initialize the MovingObject the instantiation must be
    passed parameters as follows

    Parameters
    ----------
    *args : Tuple of floats
        ( ( (top_left_x), (top_left_y) ),
        ( (bottom_right_x), (bottom_right_y) ) )

    Example
    -------
    >>>> obj_1 = MovingObject(((1, 5), (1.6, 5.6)))

    """
    def __init__(self, *args):
        self._coordinates = AttrDict()
        self._coordinates.top = AttrDict()
        self._coordinates.bottom = AttrDict()
        self._coordinates.top.left = AttrDict(
                                     {'x': float(args[0][0]),
                                      'y': float(args[0][1])})
        self._coordinates.top.right = AttrDict(
                                     {'x': float(args[1][0]),
                                      'y': float(args[0][1])})
        self._coordinates.bottom.left = AttrDict(
                                     {'x': float(args[0][0]),
                                      'y': float(args[1][1])})
        self._coordinates.bottom.right = AttrDict(
                                     {'x': float(args[1][0]),
                                      'y': float(args[1][1])})

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def top(self):
        return AttrDict({'left': self._coordinates.top.left,
                         'right': self._coordinates.top.right})

    @property
    def bottom(self):
        return AttrDict({'left': self._coordinates.bottom.left,
                         'right': self._coordinates.bottom.right})

    @property
    def left(self):
        return AttrDict({'top': self._coordinates.top.left,
                         'bottom': self._coordinates.bottom.left})

    @property
    def right(self):
        return AttrDict({'top': self._coordinates.top.right,
                         'bottom': self._coordinates.bottom.right})

    def merge(self, merge_with, noise_smoothing_percent):
        #
        # These coords are in screen coords, so > means
        # "lower than" and "further right than".  And <
        # means "higher than" and "further left than".
        #
        # We also inflate the box size by 10% to deal with
        # fuzziness in the data.  (Without this, there are many times a bbox
        # is short of overlap by just one or two pixels.)
        #
        Increase = 1 + noise_smoothing_percent
        Reduce = 1 - noise_smoothing_percent
        if (self.bottom.right.x*Increase > merge_with.top.left.x*Reduce) and \
           (self.bottom.right.y*Increase > merge_with.top.left.y*Reduce) and \
           (self.top.left.x*Reduce < merge_with.bottom.right.x*Increase) and \
           (self.top.left.y*Reduce < merge_with.bottom.right.y*Increase):

            new_coordinates = (((min(self.top.left.x,
                                     merge_with.top.left.x),
                                 min(self.top.left.y,
                                     merge_with.top.left.y)),
                                (max(self.bottom.right.x,
                                     merge_with.bottom.right.x),
                                 max(self.bottom.right.y,
                                     merge_with.bottom.right.y))))

            # TODO Need to make this delete the acutal instance
            del merge_with # TODO Need to make this delete the acutal instance
            del self # TODO Need to make this delete the acutal instance
            return MovingObject(*new_coordinates)
        else:
            return False

#    @coordinates.setter
#    def coordinates(self, values):
#        self._coordinates.update[values]
        
# %%
#        self = AttrDict({'top': None, 'bottom': None})
#        self.top = AttrDict({'left': None, 'right': None})
#        self.bottom = AttrDict({'left': None, 'right': None})
#        self.top.left = AttrDict({'x': 0, 'y': 0})
#        self.top.right = AttrDict({'x': 0, 'y': 0})
#        self.bottom.left = AttrDict({'x': 0, 'y': 0})
#        self.bottom.right = AttrDict({'x': 0, 'y': 0})