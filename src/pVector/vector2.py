from typing import overload, ClassVar, Self

class Vector2:
    """A class for handling the storage and math behind vectors in 2d space"""

    #Define the class attributes so intellisense can see them
    ZERO: ClassVar["Vector2"]
    ONE: ClassVar["Vector2"]
    UP: ClassVar["Vector2"]
    DOWN: ClassVar["Vector2"]
    LEFT: ClassVar["Vector2"]
    RIGHT: ClassVar["Vector2"]
    NEGATIVE_INFINITE: ClassVar["Vector2"]
    INFINITE: ClassVar["Vector2"]

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

    #Math Methods
    def length_squared(self) -> float:
        """Returns the length of this vector squared"""
        return self.x ** 2 + self.y ** 2
    def length(self) -> float:
        """Returns the length of this vector"""
        return self.length_squared() ** 0.5
    def normalized(self) -> Self:
        """Returns a new vector in the same direction of the original but with a `magnitude` or `length` of 1"""
        divisor = self.length()
        return Vector2(self.x / divisor, self.y / divisor)

    #Dunder Methods
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
    def __str__(self):
        return f"Vector2({self.x}, {self.y})"
    def __len__(self):
        return self.length()
    def __eq__(self, other):
        if str(type(other)) not in (str(type(Vector2)), "<class '_FrozenVector2'>"): raise TypeError(f"Cannot compare type Vector2 with type {type(other)}")
        return [self.x, self.y] == [other.x, other.y]
    def __ne__(self, other):
        if str(type(other)) not in (str(type(Vector2)), "<class '_FrozenVector2'>"): raise TypeError(f"Cannot compare type Vector2 with type {type(other)}")
        return [self.x, self.y] != [other.x, other.y]
    def __lt__(self, other):
        if str(type(other)) not in (str(type(Vector2)), "<class '_FrozenVector2'>"): raise TypeError(f"Cannot compare type Vector2 with type {type(other)}")
        return self.length_squared() < other.length_squared()
    def __le__(self, other):
        if str(type(other)) not in (str(type(Vector2)), "<class '_FrozenVector2'>"): raise TypeError(f"Cannot compare type Vector2 with type {type(other)}")
        return self.length_squared() <= other.length_squared()
    def __gt__(self, other):
        if str(type(other)) not in (str(type(Vector2)), "<class '_FrozenVector2'>"): raise TypeError(f"Cannot compare type Vector2 with type {type(other)}")
        return self.length_squared() > other.length_squared()
    def __ge__(self, other):
        if str(type(other)) not in (str(type(Vector2)), "<class '_FrozenVector2'>"): raise TypeError(f"Cannot compare type Vector2 with type {type(other)}")
        return self.length_squared() >= other.length_squared()

    #For immutable/Frozen vectors
    def freeze(self):
        """This will return a new vector2 with the exact same `x` and `y` values of this one, that is immutable"""
        class _FrozenVector2(Vector2):
            "A frozen/immutable Vector2"
            def __init__(self, x, y):
                object.__setattr__(self, '_Vector2__x', x)
                object.__setattr__(self, '_Vector2__y', y)
            def __setattr__(self, name, value):
                raise AttributeError("This Vector2 instance is immutable")
        return _FrozenVector2(self.x, self.y)
    
    #Aliases
    i = x
    j = y
    magnitude = length

#Set the value for the constant class attributes, and freeze them
Vector2.ZERO = Vector2(0).freeze()
Vector2.ONE = Vector2(1).freeze()
Vector2.UP = Vector2(0, 1).freeze()
Vector2.DOWN = Vector2(0, -1).freeze()
Vector2.LEFT = Vector2(-1, 0).freeze()
Vector2.RIGHT = Vector2(1, 0).freeze()
Vector2.NEGATIVE_INFINITE = Vector2(float("-inf")).freeze()
Vector2.INFINITE = Vector2(float("inf")).freeze()

#Delete the now unneeded imports
del overload, ClassVar, Self