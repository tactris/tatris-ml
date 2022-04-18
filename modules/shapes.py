import numpy as np


SHAPES = {
    "L1": np.array([[1, 0], [1, 0], [1, 1]]),
    "L2": np.array([[0, 0, 1], [1, 1, 1]]),
    "L3": np.array([[1, 1], [0, 1], [0, 1]]),
    "L4": np.array([[1, 1, 1], [1, 0, 0]]),
    "J1": np.array([[1, 0, 0], [1, 1, 1]]),
    "J2": np.array([[0, 1], [0, 1], [1, 1]]),
    "J3": np.array([[1, 1, 1], [0, 0, 1]]),
    "J4": np.array([[1, 1], [1, 0], [1, 0]]),
    "Z1": np.array([[0, 1], [1, 1], [1, 0]]),
    "Z2": np.array([[1, 1, 0], [0, 1, 1]]),
    "S1": np.array([[1, 0], [1, 1], [0, 1]]),
    "S2": np.array([[0, 1, 1], [1, 1, 0]]),
    "T1": np.array([[0, 1, 0], [1, 1, 1]]),
    "T2": np.array([[1, 0], [1, 1], [1, 0]]),
    "T3": np.array([[1, 1, 1], [0, 1, 0]]),
    "T4": np.array([[0, 1], [1, 1], [0, 1]]),
    "O1": np.array([[1, 1], [1, 1]]),
    "I1": np.array([[1], [1], [1], [1]]),
    "I2": np.array([[1, 1, 1, 1]]),
}


class Shape:
    def __init__(self, name: str):
        self.name = name
        self.shape = SHAPES[name]

    @classmethod
    def get_random_shape(cls, *shapes: 'Shape') -> 'Shape':
        available_shapes = set(SHAPES.keys())
        if shapes:
            available_shapes -= set(shape.name for shape in shapes)
        shape_name = np.random.choice(tuple(available_shapes))
        return cls(shape_name)

    @property
    def hash(self) -> np.array:
        return self.shape

    @property
    def height(self):
        return len(self.shape)

    @property
    def width(self):
        return len(self.shape[0])

    def rich(self) -> str:
        result = ""
        for i in range(0, 4):
            for j in range(0, 4):
                try:
                    if self.shape[i][j]:
                        result += "🟪"
                    else:
                        result += "  "
                except IndexError:
                    result += "  "
            result += "\n"
        return result

    def __repr__(self) -> str:
        return self.name
