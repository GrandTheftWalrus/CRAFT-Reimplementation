import numpy as np
import cv2
import math
from math import exp

# To whomst it may concern, all this code does is enlarge a box whilst
# ensuring its corners don't go out of bounds of (h, w) but the author
# wrote this code did it in such an overly complicated way lul


# This function calculates the angle (in radians) between two points
# Apoint and Bpoint with respect to the X-axis. It uses the arctangent
# function to find the angle. It's important to note that this
# implementation avoids division by zero by adding a small constant
# (10e-8) to the denominator.
def pointAngle(Apoint, Bpoint):
    angle = (Bpoint[1] - Apoint[1]) / ((Bpoint[0] - Apoint[0]) + 10e-8)
    return angle


# This function calculates the Euclidean distance between two points
# Apoint and Bpoint. It uses the Pythagorean theorem to compute the distance.
def pointDistance(Apoint, Bpoint):
    return math.sqrt((Bpoint[1] - Apoint[1]) ** 2 + (Bpoint[0] - Apoint[0]) ** 2)


# This function calculates the slope (K) and y-intercept (B) of the line
# passing through two points Apoint and Bpoint. It calls pointAngle to
# calculate the slope and then uses that slope to find the y-intercept.
def lineBiasAndK(Apoint, Bpoint):
    K = pointAngle(Apoint, Bpoint)
    B = Apoint[1] - K * Apoint[0]
    return K, B


def getX(K, B, Ypoint):
    return int((Ypoint - B) / K)


# This function calculates a new point (x1, y1) based on two input points
# Apoint and Bpoint and their relationship to a bounding box defined by
# height (h) and width (w). The new point is determined by extending or
# shrinking a line segment between the input points in one of four possible
# directions based on the placehold argument (e.g., "leftTop," "rightTop,"
# "rightBottom," "leftBottom"). The angle and distance between the points
# are used to calculate the new point's coordinates.
def sidePoint(Apoint, Bpoint, h, w, placehold):
    K, B = lineBiasAndK(Apoint, Bpoint)
    angle = abs(math.atan(pointAngle(Apoint, Bpoint)))
    distance = pointDistance(Apoint, Bpoint)

    halfIncreaseDistance = 1.0 * distance  # this was originally 0.5 but I changed it

    XaxisIncreaseDistance = abs(math.cos(angle) * halfIncreaseDistance)
    YaxisIncreaseDistance = abs(math.sin(angle) * halfIncreaseDistance)

    if placehold == "leftTop":
        x1 = max(0, Apoint[0] - XaxisIncreaseDistance)
        y1 = max(0, Apoint[1] - YaxisIncreaseDistance)
    elif placehold == "rightTop":
        x1 = min(w, Bpoint[0] + XaxisIncreaseDistance)
        y1 = max(0, Bpoint[1] - YaxisIncreaseDistance)
    elif placehold == "rightBottom":
        x1 = min(w, Bpoint[0] + XaxisIncreaseDistance)
        y1 = min(h, Bpoint[1] + YaxisIncreaseDistance)
    elif placehold == "leftBottom":
        x1 = max(0, Apoint[0] - XaxisIncreaseDistance)
        y1 = min(h, Apoint[1] + YaxisIncreaseDistance)

    return int(x1), int(y1)


# This function takes a list box containing four points representing the
# corners of a rectangle and the height (h) and width (w) of the bounding
# box. It first calculates the intersection point of the diagonals of the
# rectangle to find the center. Then, it uses sidePoint to calculate the new
# positions of the rectangle's corners after enlarging or shrinking the
# rectangle while keeping the center point fixed. The resulting new
# coordinates are returned as a numpy array.
def enlargebox(box, h, w):
    # box = [Apoint, Bpoint, Cpoint, Dpoint]
    Apoint, Bpoint, Cpoint, Dpoint = box
    K1, B1 = lineBiasAndK(box[0], box[2])
    K2, B2 = lineBiasAndK(box[3], box[1])
    X = (B2 - B1) / (K1 - K2)
    Y = K1 * X + B1
    center = [X, Y]

    x1, y1 = sidePoint(Apoint, center, h, w, "leftTop")
    x2, y2 = sidePoint(center, Bpoint, h, w, "rightTop")
    x3, y3 = sidePoint(center, Cpoint, h, w, "rightBottom")
    x4, y4 = sidePoint(Dpoint, center, h, w, "leftBottom")
    newcharbox = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
    return newcharbox
