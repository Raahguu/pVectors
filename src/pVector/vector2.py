from typing import overload, ClassVar, Self
import math

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
    E: ClassVar["Vector2"]
    PI: ClassVar["Vector2"]

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
    @overload
    def __init__(self, vector : Self) -> None:
        """Creates a copy of the given vector"""
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
            elif isinstance(args[0], Self):
                self.x = args[0].x
                self.y = args[0].y
            else:
                 TypeError("Excpected either (x, y), (value), ([x, y]), or (vector2)")
        elif len(args) == 2:
            self.x, self.y = float(args[0]), float(args[1])
        else:
            raise TypeError("Excpected either (x, y), (value), ([x, y]), or (vector2)")


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
    @property
    def angle(self) -> float:
        """The angle in randians clockwise from (1, 0) to this vector. Ranges from [pi, -pi)"""
        return math.atan2(self.y, self.x)
    @angle.setter
    def angle(self, value : float):
        value = float(value)
        if value > math.pi or value < -math.pi: raise ValueError("The angle os a `Vector2` must be within [pi, -pi)]")
        length = self.magnitude()
        self.x = math.sin(value) * length
        self.y = math.cos(value) * length

    #Math Methods
    def magnitude_squared(self : Self) -> float:
        """Returns the length of this vector squared"""
        return self.x ** 2 + self.y ** 2
    def magnitude(self : Self) -> float:
        """Returns the length of this vector"""
        return math.sqrt(self.magnitude_squared())
    def normalized(self : Self) -> Self:
        """Returns a new vector in the same direction of the original but with a `magnitude` or `length` of 1"""
        divisor = self.magnitude()
        return Vector2(self.x / divisor, self.y / divisor)
    def dot(a : Self, b : Self) -> Self:
        return a.x * b.x + a.y * b.y

    def angle_between(origin : Self, target : Self) -> float:
        """Returns the angle in radians between two vectors"""
        dot_product = origin.dot(target)
        len_product = origin.magnitude() * target.magnitude()
        if len_product == 0: raise ValueError("Cannot calculate angle with zero-length vector")
        return math.acos(dot_product / len_product)
    
    def distance_between_squared(orgin : Self, target : Self) -> float:
        """Resturns the distance squared between two vectors"""
        return (orgin - target).magnitude_squared()
    def distance_between(a : Self, b : Self) -> float:
        """Returns the distance between two vectors"""
        return math.sqrt(a.distance_between_squared(b))
    
    def clamp_magnitude(original : Self, max_magnitude : float | int) -> Self:
        """Returns a copy of the vector with its magnitude clamped"""
        length = original.magnitude()
        if length <= max: return Vector2(original)
        return Vector2(original.x / length * max_magnitude , original.y / length * max_magnitude)
    def clamp_magnitude_squared(original : Self, max_magnitude_squared : float | int) -> Self:
        """Returns a copy of the vector with its magnitue squared capped"""
        length_squared = original.magnitude_squared()
        if length_squared <= max: return Vector2(original)
        return Vector2(original.x / length_squared * max_magnitude_squared , original.y / length_squared * max_magnitude_squared)
    
    def clamp(original : Self, minimum : Self, maximum : Self) -> Self:
        """Returns a clamped copy of the vector between a maximum and minimum vector"""
        min_angle = minimum.angle
        max_angle = maximum.angle
        original_angle = original.angle
        if max_angle < min_angle: raise ValueError("The maxium vector's angle must be larger then the minimum vector's")
        if original_angle < min_angle: return Vector2(minimum)
        if original_angle > max_angle: return Vector2(maximum)
        else: return Vector2(original)
    
    def lerp(original : Self, target : Self, t : float) -> Self:
        """Linearly interpolates between two vectors by `t`. The paramater `t` is clamped to the range [0, 1]"""
        if t < 0: t = 0
        elif t > 1: t = 1
        return original + (target - original) *  t
    def lerp_unclamped(original : Self, target : Self, t : float) -> Self:
        """Linearly interpolates between two vectors by `t`. The paramater `t` is unclamped"""
        return original + (target - original) * t
    
    def max(a : Self, b : Self) -> Self:
        """Returns a vector that is made from the largest components of two vectors"""
        return Vector2(max(a.x, b.x), max(a.y, b.y))
    def min(a : Self, b : Self) -> Self:
        """Returns a vector that is made from the smallest components of two vectors"""
        return Vector2(min(a.x, b.x), min(a.y, b.y))
    
    def unit_vector_towards(origin : Self, target : Self) -> Self:
        """Returns a unit vector pointing in the direction towards the `target` from the `origin`"""
        return (target - origin).normalized()
    
    def perpendicular(original : Self):
        """Returns the vector perpendicular to this one (rotated 90 degrees counter-clockwise)"""
        return Vector2(-original.y, original.x)
    def project(a : Self, b : Self) -> Self:
        """Returns the vector projection of `a` onto `b`"""
        return (a * b) / b.magnitude_squared() * b
    def reflect(original : Self, normal : Self):
        """Reflects this vector across the given normal vector"""
        return original - 2 * Vector2.project(original, normal)
    def scale(a : Self, b : Self) -> Self:
        """Returns the mutliple of two vectors component wise"""
        return Vector2(a.x * b.x, a.y * b.y)
    
    def degrees_to_radians(degrees : float) -> float:
        """Converts degrees to radians"""
        return degrees * math.pi / 180
    def radians_to_degrees(radians : float) -> float:
        """Converts radians to degrees"""
        return radians * 180 / math.pi

    #Dunder Methods
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
    def __str__(self):
        return f"Vector2({self.x}, {self.y})"
    def __iter__(self):
        return iter((self.x, self.y))
    def __bool__(self):
        return True if  self.x != 0 or self.y != 0 else False
    def __complex__(self):
        return complex(self.x, self.y)
    def __len__(self):
        return self.magnitude()
    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))
    def __round__(self, n : int):
        if type(n) != int: raise TypeError("Must round to an `int` number of decimal places")
        return Vector2(round(self.x, n), round(self.y, n))
    def __hash__(self):
        return hash([self.x, self.y])
    
    def __eq__(self, other : Self):
        if type(other) != Vector2: raise TypeError(f"Cannot compare type `Vector2` with type `{type(other)}`")
        return [self.x, self.y] == [other.x, other.y]
    def __ne__(self, other : Self):
        if type(other) != Vector2: raise TypeError(f"Cannot compare type `Vector2` with type `{type(other)}`")
        return [self.x, self.y] != [other.x, other.y]
    def __lt__(self, other : Self):
        if type(other) != Vector2: raise TypeError(f"Cannot compare type `Vector2` with type `{type(other)}`")
        return self.magnitude_squared() < other.magnitude_squared()
    def __le__(self, other : Self):
        if type(other) != Vector2: raise TypeError(f"Cannot compare type `Vector2` with type `{type(other)}`")
        return self.magnitude_squared() <= other.magnitude_squared()
    def __gt__(self, other : Self):
        if type(other) != Vector2: raise TypeError(f"Cannot compare type `Vector2` with type `{type(other)}`")
        return self.magnitude_squared() > other.magnitude_squared()
    def __ge__(self, other : Self):
        if type(other) != Vector2: raise TypeError(f"Cannot compare type `Vector2` with type `{type(other)}`")
        return self.magnitude_squared() >= other.magnitude_squared()
    
    def __add__(self, other):
        if type(other) == Vector2: return Vector2(self.x + other.x, self.y + other.y)
        elif type(other) in (int, float): return Vector2(self.x + other, self.y + other)
        elif type(other) in (list, tuple):
            if len(other) == 2: return Vector2(self.x + other[0], self.y + other[1])
            else: raise ValueError(f"When adding type `Vector2` and type `{type(other)}`, then the `{type(other)}` must be of length 2")
        else: raise TypeError(f"Cannot add type `Vector2` and type `{type(other)}`")
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if type(other) == Vector2: return Vector2(self.x - other.x, self.y - other.y)
        elif type(other) in (int, float): return Vector2(self.x - other, self.y - other)
        elif type(other) in (list, tuple):
            if len(other) == 2: return Vector2(self.x - other[0], self.y - other[1])
            else: raise ValueError(f"When minusing type `Vector2` and type `{type(other)}`, then the `{type(other)}` must be of length 2")
        else: raise TypeError(f"Cannot minus type `Vector2` and type `{type(other)}`")
    def __rsub__(self, other):
        if type(other) == Vector2: return Vector2(other.x - self.x, other.y - self.y)
        elif type(other) in (int, float): return Vector2(other - self.x, other - self.y)
        elif type(other) in (list, tuple):
            if len(other) == 2: return Vector2(other[0] - self.x, other[1] - self.y)
            else: raise ValueError(f"When minusing type `{type(other)}` and type `Vector2`, then the `{type(other)}` must be of length 2")
        else: raise TypeError(f"Cannot minus type `{type(other)}` and type `Vector2`")
    
    def __mul__(self, other):
        if type(other) == Vector2: return self.dot(other)
        elif type(other) in (int, float): return Vector2(self.x * other, self.y * other) # scalar mutliplication
        elif type(other) in (list, tuple):
            if len(other) == 2: return self.dot(Vector2(other))
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
    
    #some import specific dunder methods
    def __trunc__(self):
        return Vector2(math.trunc(self.x), math.trunc(self.y))
    def __floor__(self):
        return Vector2(math.floor(self.x), math.floor(self.y))
    def __ceil__(self):
        return Vector2(math.ceil(self.x), math.ceil(self.y))
    def __deepcopy__(self, memo=None):
        return Vector2(self)
    

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

#Set the value for the constant class attributes, and freeze them
Vector2.ZERO = Vector2(0).freeze()
Vector2.ONE = Vector2(1).freeze()
Vector2.UP = Vector2(0, 1).freeze()
Vector2.DOWN = Vector2(0, -1).freeze()
Vector2.LEFT = Vector2(-1, 0).freeze()
Vector2.RIGHT = Vector2(1, 0).freeze()
Vector2.NEGATIVE_INFINITE = Vector2(float("-inf")).freeze()
Vector2.INFINITE = Vector2(float("inf")).freeze()
Vector2.E = Vector2(math.e).freeze()
Vector2.PI = Vector2(math.pi).freeze()

#Delete the now unneeded imports
del overload, ClassVar, Self, math