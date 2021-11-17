import shapefile
import math

def pointToLineDistance(point, lineStart, lineEnd):
    # Returns the distance of the line from the perspective of the point
    # Defining the three points in x and y (lon and lat).
    px = point[0]
    py = point[1]
    x1 = lineStart[0]
    y1 = lineStart[1]
    x2 = lineEnd[0]
    y2 = lineEnd[1]

    if x2 - x1 == 0: # Handling the case of a horizontal line
        return math.fabs(px - x1)
    if y2 - y1 == 0: # Handling the case of a vertical line
        return math.fabs(py - y1)

    k = (y2 - y1) / (x2 - x1)
    b = y1 - k * x1
    return math.fabs(k * px - py + b) / math.pow(k * k + 1, 0.5)


def DouglasPeucker(line, epsilon):
    dmax = 0
    index = 0
    for i in range(1, len(line) - 1):
        d = pointToLineDistance(line[i], line[0], line[-1])
        if d > dmax:
            index = i
            dmax = d

    if dmax > epsilon:
        simplifiedLine = DouglasPeucker(line[:index+1], epsilon)[:-1] + DouglasPeucker(line[index:], epsilon)
    else:
        simplifiedLine = [line[0], line[-1]]

    return simplifiedLine

##############################################
shpFile = shapefile.Reader("shapeFileData/SmallLine")
line = shpFile.shape(0).points


tolerance = 100

simplifiedLine = DouglasPeucker(line, tolerance)

w =  shapefile.Writer("output")
w.field('fieldName', 'C')
w.record()
w.line([simplifiedLine])
w.close()

w = shapefile.Writer(dbf='output.dbf')
w.field('fieldName', 'C')
w.record()
w.close()