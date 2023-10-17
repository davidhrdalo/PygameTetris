# File is for defining Tetrominoes AKA Tetris Shapes
# Normal shapes are defined followed by the extended game shapes
# The classes create an instance for the tetromino and assign them a colour
# The shapes are converted in the convert_shape function in the controller

# Defining standard tetromino colours
Green = (0, 255, 0)
Red = (255, 0, 0)
Cyan = (0, 255, 255)
Yellow = (255, 255, 0)
Orange = (255, 165, 0)
Blue = (0, 0, 255)
Purple = (128, 0, 128)

# Normal Tetris shapes
# I tetromino
class ITetromino:
    SHAPES = [
            [['*', 'O', '*', '*', '*'],
            ['*', 'O', '*', '*', '*'],
            ['*', 'O', '*', '*', '*'],
            ['*', 'O', '*', '*', '*'],
            ['*', '*', '*', '*', '*']],

            [['O', 'O', 'O', 'O', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*']]
    ]
    COLOUR = Cyan

# L tetromino
class LTetromino:
    SHAPES = [
            [['*', '*', '*', '*', '*'],
            ['*', '*', '*', 'O', '*'],
            ['*', 'O', 'O', 'O', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', 'O', 'O', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', 'O', 'O', 'O', '*'],
            ['*', 'O', '*', '*', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', 'O', 'O', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', '*', '*', '*']]]

    COLOUR = Blue

# J tetromino
class JTetromino:
    SHAPES = [
            [['*', '*', '*', '*', '*'],
            ['*', 'O', '*', '*', '*'],
            ['*', 'O', 'O', 'O', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', '*', 'O', 'O', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', 'O', 'O', 'O', '*'],
            ['*', '*', '*', 'O', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', 'O', 'O', '*', '*'],
            ['*', '*', '*', '*', '*']]]

    COLOUR = Orange

# O tetromino
class OTetromino:
    SHAPES = [
            [['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', 'O', 'O', '*', '*'],
            ['*', 'O', 'O', '*', '*'],
            ['*', '*', '*', '*', '*']]]

    COLOUR = Yellow

# S tetromino
class STetromino:
    SHAPES = [
            [['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', '*', 'O', 'O', '*'],
            ['*', 'O', 'O', '*', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', 'O', 'O', '*'],
            ['*', '*', '*', 'O', '*'],
            ['*', '*', '*', '*', '*']]]

    COLOUR = Green

# T tetromino
class TTetromino:
    SHAPES = [
            [['*', '*', '*', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', 'O', 'O', 'O', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', 'O', 'O', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', 'O', 'O', 'O', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', 'O', 'O', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', '*', '*', '*']]]

    COLOUR = Purple

# Z tetromino
class ZTetromino:
    SHAPES = [
            [['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', 'O', 'O', '*', '*'],
            ['*', '*', 'O', 'O', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', 'O', 'O', '*', '*'],
            ['*', 'O', '*', '*', '*'],
            ['*', '*', '*', '*', '*']]]

    COLOUR = Red

# Extended Tetris shapes
# Small / Extended I tetromino
class E_ITetromino:
    SHAPES = [
            [['*', '*', '*', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', 'O', 'O', 'O', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*']]]

    COLOUR = Cyan

# Small / Extended L tetromino
class E_LTetromino:
    SHAPES = [
            [['*', '*', '*', '*', '*'],
            ['*', '*', '*', 'O', '*'],
            ['*', '*', 'O', 'O', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', 'O', 'O', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', 'O', 'O', '*', '*'],
            ['*', 'O', '*', '*', '*'],
            ['*', '*', '*', '*', '*']],

            [['*', '*', '*', '*', '*'],
            ['*', 'O', 'O', '*', '*'],
            ['*', '*', 'O', '*', '*'],
            ['*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*']]]

    COLOUR = Blue

class Tetromino:
    def __init__(self, x_pos, y_pos, shape, colour):
        self.spin = 0
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.shape = shape
        self.colour = colour

    def copy(self):
        return Tetromino(self.x_pos, self.y_pos, self.shape, self.spin)
    def width(self):
        return len(self.shape[0])

class TetrominoFactory:
    """ TetrominoFactory is responsible for creating Tetrominoes """
    tetromino_classes = {
        'I': ITetromino,
        'L': LTetromino,
        'J': JTetromino,
        'O': OTetromino,
        'S': STetromino,
        'T': TTetromino,
        'Z': ZTetromino,
    }

    extended_tetromino_classes = {
        'E_I': E_ITetromino,
        'E_L': E_LTetromino,
    }
    @classmethod
    def add_extended_tetrominoes(cls):
        """Method allows for the use of all tetromino shapes including extended shapes"""
        cls.tetromino_classes.update(cls.extended_tetromino_classes)

    @staticmethod
    def create_tetromino(type, x_pos, y_pos):
        """Static method to create a Tetromino instance"""
        if type in TetrominoFactory.tetromino_classes:
            tetromino_class = TetrominoFactory.tetromino_classes[type]
            return Tetromino(x_pos, y_pos, tetromino_class.SHAPES, tetromino_class.COLOUR)
        else:
            raise ValueError(f"Unknown Tetromino type: {type}")
