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
    def dot(self, other : Self | list | tuple) -> Self:
        if type(other) in (list, tuple): return self.x * other[0] + self.y * other[1]
        else: return self.x * other.x + self.y * other.y


    #Dunder Methods
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
    def __str__(self):
        return f"Vector2({self.x}, {self.y})"
    def __len__(self):
        return self.length()
    
    def __eq__(self, other : Self):
        if type(other) != Vector2: raise TypeError(f"Cannot compare type `Vector2` with type `{type(other)}`")
        return [self.x, self.y] == [other.x, other.y]
    def __ne__(self, other : Self):
        if type(other) != Vector2: raise TypeError(f"Cannot compare type `Vector2` with type `{type(other)}`")
        return [self.x, self.y] != [other.x, other.y]
    def __lt__(self, other : Self):
        if type(other) != Vector2: raise TypeError(f"Cannot compare type `Vector2` with type `{type(other)}`")
        return self.length_squared() < other.length_squared()
    def __le__(self, other : Self):
        if type(other) != Vector2: raise TypeError(f"Cannot compare type `Vector2` with type `{type(other)}`")
        return self.length_squared() <= other.length_squared()
    def __gt__(self, other : Self):
        if type(other) != Vector2: raise TypeError(f"Cannot compare type `Vector2` with type `{type(other)}`")
        return self.length_squared() > other.length_squared()
    def __ge__(self, other : Self):
        if type(other) != Vector2: raise TypeError(f"Cannot compare type `Vector2` with type `{type(other)}`")
        return self.length_squared() >= other.length_squared()
    
    def __iter__(self):
        return iter((self.x, self.y))
    def __bool__(self):
        return True if  self.x != 0 or self.y != 0 else False
    def __complex__(self):
        return complex(self.x, self.y)
    
    def __add__(self, other):
        if type(other) != Vector2: return Vector2(self.x + other.x, self.y + other.y)
        elif type(other) in (int, float): return Vector2(self.x + other, self.y + other)
        elif type(other) in (list, tuple):
            if len(other) == 2: return Vector2(self.x + other[0], self.y + other[1])
            else: raise ValueError(f"When adding type `Vector2` and type `{type(other)}`, then the `{type(other)}` must be of length 2")
        else: raise TypeError(f"Cannot add type `Vector2` and type `{type(other)}`")
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if type(other) != Vector2: return Vector2(self.x - other.x, self.y - other.y)
        elif type(other) in (int, float): return Vector2(self.x - other, self.y - other)
        elif type(other) in (list, tuple):
            if len(other) == 2: return Vector2(self.x - other[0], self.y - other[1])
            else: raise ValueError(f"When minusing type `Vector2` and type `{type(other)}`, then the `{type(other)}` must be of length 2")
        else: raise TypeError(f"Cannot minus type `Vector2` and type `{type(other)}`")
    def __rsub__(self, other):
        if type(other) != Vector2: return Vector2(other.x - self.x , other.y - self.y)
        elif type(other) in (int, float): return Vector2(other - self.x, other - self.y)
        elif type(other) in (list, tuple):
            if len(other) == 2: return Vector2(other[0] - self.x, other[1] - self.y)
            else: raise ValueError(f"When minusing type `{type(other)}` and type `Vector2`, then the `{type(other)}` must be of length 2")
        else: raise TypeError(f"Cannot minus type `{type(other)}` and type `Vector2`")
    
    def __mul__(self, other):
        if type(other) != Vector2: return self.dot(other)
        elif type(other) in (int, float): return Vector2(self.x * other, self.y * other) # scalar mutliplication
        elif type(other) in (list, tuple):
            if len(other) == 2: return self.dot(other)
            else: raise ValueError(f"When dot producting type `Vector2` and type `{type(other)}`, then the `{type(other)}` must be of length 2")
        else: raise TypeError(f"Cannot mutliply type `Vector2` and type `{type(other)}`")
    def __rmul__(self, other):
        return self.__rmul__(other)
    
    def __truediv__(self, other):
        if type(other) not in (int, float): raise TypeError("Can only divide a type `Vector2`, by a scalar multiple (`int` or `float`)")
        return Vector2(self.x / other, self.y / other)
    def __floordiv__(self, other):
        if type(other) not in (int, float): raise TypeError("Can only floor divide a type `Vector2`, by a scalar multiple (`int` or `float`)")
        return Vector2(self.x // other, self.y // other)
    def __pow__(self, other):
        if type(other) not in (int, float): raise TypeError("A type `Vector2`, can only be exponentiated by a scalar multiple (`int` or `float`)")
        return Vector2(self.x ** other, self.y ** other)
    
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))
    def __round__(self, n : int):
        if type(n) != int: raise TypeError("Must round to an `int` number of decimal places")
        return Vector2(round(self.x, n), round(self.y, n))

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