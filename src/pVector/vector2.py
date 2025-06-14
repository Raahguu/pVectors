from typing import overload, ClassVar, Self

class Vector2:
    """A class for handling the storage and math behind vectors in 2d space"""
    @overload
    def __init__(self, x : float, y : float) -> None: 
        """Specify the `x` and `y` componets of the vector"""
        ...
    @overload
    def __init__(self, value : float) -> None:
        """`value` is assinged to both the `x` and `y` values of the vector"""
        ...
    @overload
    def __init__(self, componets : list | tuple) -> None: 
        """The `components` needs to be a iterator of length 2, containing the `x` and `y` values"""
        ...
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], (float, int, str)):
                self.x, self.y = (float(args[0]),) * 2
            elif isinstance(args[0], (list, tuple)):
                components = args[0]
                if len(components) != 2:
                    raise TypeError("Expected a list or tuple of length 2")
                self.x, self.y = float(components[0]), float(components[1])
        elif len(args) == 2:
            self.x, self.y = float(args[0]), float(args[1])
        else:
            raise TypeError("Excpected either (x, y), (value), or ([x, y])")

    #Getters and Setters
    @property
    def x(self) -> float:
        return self.__x
    @x.setter
    def x(self, value : float):
        value = float(value)
        self.__x = value
    @property
    def y(self) -> float:
        return self.__y
    @y.setter
    def y(self, value : float):
        value = float(value)
        self.__y = value