#matrix.py
#Charles J. Lai
#August 18, 2013

import unimath

"""
======
matrix
======
This module contains a wrapper class that represents a matrix and
functions that can be used to analyze/evaluate a matrix class. 

Addition, subtraction, division, and multiplication functionality are 
implemented as cases within the appropriate functions in the unimath (core
math functions) module for Matrix class types as well as overloaded 
operators defined within the Matrix class.

Usage/Syntax
============
Creating a matrix using a constructor or setter requires the use of a 
Matlab-like syntax. For example, a 3*3 matrix:

                                1 2 3
                                3 2 1
                                5 1 4
        
has a raw string expression using Matlab syntax: "1,2,3;3,2,1;5,1,4"
with no spaces, using semi-colons to separate rows, and commas to
separate elements within each row. X and Y coordinates also mimic
Matlab's non-zero coordinate system for traversing a matrix.

Contents
--------
* Array        - A one-dimensional array class with various methods
* Matrix       - A matrix class with various methods
* fliplr()     - Reverses an array or column of a matrix
* ref()        - Returns the row echelon form of a matrix
* rref()       - Returns the reduced row echelon form of a matrix
* trans()      - Returns the transpose of a matrix or array
* det()        - Returns the determinant of a matrix
* diag()       - Returns the diagonalized form of a matrix
* eig()        - Returns the eigenvector of a matrix
"""

class Matrix(object):
    """
    Instances represent a two-dimensional matrix.

    ===========
    Description
    ===========
    A matrix is a type of data structure that can hold two two-dimensional
    data on a discrete map of points. #ADD MORE DESCRIPTION/HISTORY#

    The actual matrix iteself is represented by a two-dimensional list
    wrapped in this matrix class which provides methods and properties
    for various matrix-based applications and analysis. Our implementation
    was created with Matlab-style constructors and matrix traversals in
    mind. This syntax is familiar with most people and thus a solid design
    decision for this module/package.

    Coordinate positions in the matrix start with ones (for example, the
    top left value in a matrix is at coordinate point [1, 1]).

               [1, 1]   <-----  1 2 3 4 5 
                                1 2 3 4 5
                                1 2 3 4 5
                                1 2 3 4 5
                                1 2 3 4 5

    The number of rows is denoted by the "m" property value and the number
    of columns is denoted by the "n" property value (again familiar notation
    for most people). The entire matrix object is of size m x n.

    Each matrix contains a variety of different methods for adding,
    subtracting, setting, and getting values/rows/columns as well as
    overloaded operatros for matrix scalar addition/subtraction in 
    addition to matrix multiplication and division.

    Note: Addition, subtraction, multiplication, and division can also be done
    with add(), sub(), mult(), div() from the unimath module in the core package.
    """
    #Properties
    _matrix = None
    _m = 0
    _n = 0
    _is_square = False

    @property 
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, raw_matrix):
        self._matrix = raw_matrix

    @property #immutable
    def m(self):
        return self._m

    @property #immutable
    def n(self):
        return self._n

    @property #immutable
    def is_square(self):
        return self._is_square

    #Constructor
    def __init__(self, raw_matrix):
        """
        Constructor: Create a new instance of a Matrix
        
        Precondition: raw_matrix is a valid matrix input according to the
        description in the meta documentation.
        """
        #Set and check the matrix
        self._parse(raw_matrix)
        self._check()

    #Built-In Methods/Operator Overloading
    def __add__(self):
        """
        """
        pass

    def __sub__(self):
        """
        """
        pass

    def __mul__(self):
        """
        """
        pass

    def __div__(self):
        """
        """
        pass

    #Methods Proper
    def disp(self, heading = "Matrix:"):
        """
        Procedure: Prints a string representation of the matrix object
        """
        print " "
        print heading
        print " "
        #Iteratively print the elements of the matrix
        for x in range(0, self.m):
            for y in range(0, self.n):
                print '%10.3f' % self._matrix[x][y],
            print "\n"

    def get(self, x, y):
        """
        Returns: Value a specified coordinate point within the matrix.

        Precondition: x and y are valid coordinates using Matlab coordinate
        rules.
        """
        return self._matrix[x-1][y-1]

    def set(self, x, y, value):
        """
        Procedure: Sets value at a specfied coordinate point to a new value.

        Precondition:b x and y are valid coordinates using Matlab coordinate
        rules.
        """
        #Check if the value specified is a string or an actual list.
        assert type(value) == float or type(value) == int
        self._matrix[x - 1][y - 1] = value

    def add_row(self, row):
        """
        Procedure: Adds a given row to the matrix to the bottom.

        Precondition: The row must be have the same length as other rows in
        the matrix. Argument passed to row is a python list.
        """
        assert len(row) == self._n, "The row has an invalid length"
        #Add the whole row to the end of the matrix
        self._matrix = self._matrix + [row]
        self._m += 1

    def add_col(self, col):
        """
        Procedure: Adds a given col to the matrix to the right

        Precondition: The column must have the same length as other rows 
        """
        assert len(col) == self._m, "The column has an invalid length"
        #Add each element to the end of each row
        x = 0
        for y in col:
            self._matrix[x] = self._matrix[x] + [y]
            x += 1
        self._n += 1
        

    def sub_row(self, x):
        """
        Procedure: Subtracts a given row from the matrix by row number. x
        represents a specific row number.

        Precondition: x must be a valid row number
        """
        assert self._m >= x, "The row number given is too large"
        assert x > 0, "Try again with a row number > 0"
        self._matrix.remove(self._matrix[x - 1])

    def sub_col(self, y):
        """
        Procedure: Subtracts a given column from the matrix by column number.

        Precondition: y must be a valid column number.
        """
        assert self._n >= y, "The column number given is too large"
        assert y > 0, "Try again with a column number > 0"
        for x in range(0, self._m):
            self._matrix.remove(self._matrix[x][y])

    #Helper Methods
    def _parse(self, raw_matrix):
        """
        Procedure: Parses the raw_matrix string and updates the Matrix object.
        Called during object construction.

        Precondition: raw_matrix is a valid input according to the description
        in the meta documentation at the top of the document.
        """
        #Some assertions statements to QC the raw_matrix input
        assert type(raw_matrix) == str, "The matrix given is not a string"
        assert raw_matrix[0] != "[", "Use Matlab matrix notation without braces"
        #Initialize default values
        self._m = -1
        self._n = -1
        #Split the matrix up into rows of strings and set m to len(self._matrix
        self._matrix = raw_matrix.split(';')
        self._m = len(self._matrix)
        #Continue parsing the input, make rows into lists of numbers
        for x in range(0, self._m):
            self._matrix[x] = self.matrix[x].split(",")
            self._matrix[x] = list(map(float, self.matrix[x]))
        #Set n to the number of elements in each row
        self._n = len(self._matrix[0])
        #Set whether the matrix is a square matrix
        if self._m == self._n:
            self._is_square == True

    def _check(self):
        """
        Procedure: Checks if the raw input was valid by QCing the properties
        of the matrix. Called during object construction.
        """
        #Test if the rest of the rows are the same length
        for r in range(0, self.m):
            assert len(self._matrix[r]) == self._n, "Invalid row lengths"
            assert type(self._matrix[r]) == list, "Some rows aren't lists"

#======================
#   Matrix Functions
#======================
def fliplr(array):
    """
    """
    pass


def ref(matrix):
    """
    """
    pass


def rref(matrix):
    """
    """
    pass


def trans(matrix):
    """
    """
    pass


def det(matrix):
    """
    """
    pass


def diag(matrix):
    """
    """
    pass


def eig(matrix):
    """
    """
    pass
#======================
#   Property Testers
#======================

def is_square(matrix):
    """
    """
    pass


def is_li(matrix):
    """
    """
    pass

