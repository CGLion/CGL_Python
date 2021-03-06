"""
Functions for image / pixel processing
Written by Oded Erell - CG-Lion Studio (c)2020
"""

from typing import List, Tuple

"""
Compound type hint aliases:
"""
Int2 = Tuple[int, int]
Float2 = Tuple[float, float]
List_Int = List[int]
List_Int2 = List[Tuple[int, int]]
List_List_Int = List[List[int]]


def cgl_fill_int_range(begin: int, end: int, ends: bool = True) -> List_Int:
    """
    Returns a list of all integers in the range: begin - end regardless of direction.
    :param begin: int - range start number
    :param end: int - range end number
    :param ends: bool - when true the list will contain the begin and end numbers
    :return: List[int]
    """
    endi: int = int(ends)
    if end > begin:
        return list(range(begin + (1 - endi), end + endi))
    elif end < begin:
        return list(range(begin - (1 - endi), end - endi, -1))
    else:
        return []


def cgl_det(p0: Int2, p1: Int2, p2: Int2) -> int:
    """
    Returns the determinant value of a 3X3 matrix containing the supplied 2D points (considering 1 as the Z component)
    :param p0: Tuple[int, int]
    :param p1: Tuple[int, int]
    :param p2: Tuple[int, int]
    :return: intTuple[int, int]
    """
    return p0[0]*p1[1] + p0[1]*p2[0] + p1[0]*p2[1] - p0[0]*p2[1] - p0[1]*p1[0] - p1[1]*p2[0]


def cgl_get_pixel_from_uv(u: float, v: float, w: int, h: int) -> Int2:
    """
    Returns an Tuple containing 2D integer coordinates
    of the pixel corresponding to the supplied UV coordinates and image width and height in pixels.
    The supplied u and v arguments are clamped to a 0.0 - 1.0 range.
    :param u: float - [0.0 - 1.0] - Supplied U coordinate
    :param v: float - [0.0 - 1.0] - Supplied V coordinate
    :param w: int - The image width in pixels
    :param h: int - The image height in pixels
    :return: tuple[int, int]
    """
    # Clamp the UV values
    u = max(min(u, 1.0), 0.0)
    v = max(min(v, 1.0), 0.0)
    # Calculate and return pixel coordinates:
    return int(round(u * (w - 1))), int(round(v * (h - 1)))


def cgl_get_pixel_uv(x: int, y: int, w: int, h: int) -> Float2:
    """
    Return a tuple containing floats representing UV coordinates of the center of the supplied pixel.
    :param x: int - the pixel x coordinate
    :param y: int - the pixel y coordinate
    :param w: int - The image width
    :param h: int - The image Height
    :return: tuple[float, float]
    """
    px_u_step = 1.0 / w
    px_v_step = 1.0 / h
    x = int(max(min(x, w - 1), 0))
    y = int(max(min(y, h - 1), 0))
    return (x * px_u_step) + (px_u_step * 0.5), (y * px_v_step) + (px_v_step * 0.5)


def cgl_line_raster_pixels(p0: Int2, p1: Int2) -> List_Int2:
    """
    Returns a list of integer tuples
    representing 2D coordinated of the pixels plotting a line from point 0 to point 1
    as defined by the supplied p0, p1 integer tuple arguments.
    This function is based on the Bresenham line algorithm as it's explained in wikipedia:
    https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    And is expended to handle the cases where teh line slope is larger than 1 i.e delta Y is larger than delta X,
    and also cases where the the line is drawn "backwards" for a large X or Y to a small X or Y.
    :param p0: tuple[int, int] - the x,y coordinate of point 0
    :param p1: tuple[int, int] - the x,y coordinate of point 1
    :return: list[tuple[int, int]]
    """
    # store line coords in 2d array:
    ln: List_List_Int = [[p0[0], p0[1]],
                         [p1[0], p1[1]]]
    # Make sure input values ar integers:
    for i in range(2):
        for j in range(2):
            ln[i][j] = int(ln[i][j])
    # Init list of line pixel coordinates - Int tuples
    line_px: List_Int2 = []
    # Get x y delta
    d: List_Int = [ln[1][0] - ln[0][0],
                   ln[1][1] - ln[0][1]]
    # Set main iteration axis:
    mx: int = 0 if abs(d[0]) > abs(d[1]) else 1
    # Set if secondary increment is positive or negative
    inc: int = 1 if d[1 - mx] >= 0 else -1
    # Make delta values absolute
    d[0] = abs(d[0])
    d[1] = abs(d[1])
    # Set init derivation:
    di: int = (2 * d[1 - mx]) - d[mx]
    # Set secondary axis start value:
    sec: int = ln[0][1 - mx]
    # Generate main axis value range:
    mrange: range = range(ln[0][mx], ln[1][mx] + 1) if ln[0][mx] < ln[1][mx] else range(ln[0][mx], ln[1][mx] - 1, -1)
    # Interate main axis coordinate range:
    for m in mrange:
        # Define and add new pixel coordinate to list
        lnpx = [(m, sec), (sec, m)]
        line_px.append(lnpx[mx])
        # Check if next pixel has value increment in secindary axis:
        if di > 0:
            sec = sec + inc
            di = di - (2 * d[mx])
        # Update derivation:
        di = di + (2 * d[1 - mx])
    # Return output list:
    return line_px


def cgl_get_triangle_lines_raster_pixels(p0: Int2,
                                         p1: Int2,
                                         p2: Int2) -> List_Int2:
    """
    Returns a list of tuples representing the raster pixels of the contour of triangle p0, p1, p2
    :param p0: tuple[int, int] - integer x, y coordinates of pixel 0 of the triangle
    :param p1: tuple[int, int] - integer x, y coordinates of pixel 1 of the triangle
    :param p2: tuple[int, int] - integer x, y coordinates of pixel 2 of the triangle
    :return: list[tuple[int, int]]
    """
    points: List_Int2 = [p0, p1, p2]
    tri_px: List_Int2 = []
    for i in range(3):
        tri_px += (cgl_line_raster_pixels(points[i], points[(i + 1) % 3]))[1:]
    return tri_px


def cgl_get_triangle_raster_pixels(p0: Int2,
                                   p1: Int2,
                                   p2: Int2,
                                   lines: bool = True) -> List_Int2:
    """
    Returns a list of tuples representing the raster pixels of the filled area of triangle p0, p1, p2 (without contours)
    :param p0: tuple[int, int] - integer x, y coordinates of pixel 0 of the triangle
    :param p1: tuple[int, int] - integer x, y coordinates of pixel 1 of the triangle
    :param p2: tuple[int, int] - integer x, y coordinates of pixel 2 of the triangle
    :param lines: bool - when True, the output list will include the triangle contours
    :return: list[tuple[int, int]]
    """
    points: list = [p0, p1, p2]
    sorted_y: list = sorted(points, key=lambda x: x[1])
    line_a: list = cgl_line_raster_pixels(sorted_y[0], sorted_y[2])
    line_b: list = cgl_line_raster_pixels(sorted_y[0], sorted_y[1])
    line_c: list = cgl_line_raster_pixels(sorted_y[1], sorted_y[2])
    tri_fill: list = []
    y_val: int = line_a[0][1]
    for i in list(range(len(line_a)))[1:-1]:
        new_y_val: int = line_a[i][1]
        if new_y_val != y_val:
            sec_line: list = line_b if new_y_val <= line_b[-1][1] else line_c
            sec_index: int = list(zip(*sec_line))[1].index(new_y_val)
            x_vals: list = cgl_fill_int_range(line_a[i][0], sec_line[sec_index][0])
            y_vals: list = [new_y_val] * len(x_vals)
            tri_fill += zip(x_vals, y_vals)
            y_val = new_y_val
    if lines:
        outlist: list = tri_fill + line_a[:-1] + line_b[1:] + line_c[1:]
    else:
        outlist: list = tri_fill
    return outlist


def cgl_get_pixel_plot_string(canvas_corner_a: Int2,
                              canvas_corner_b: Int2,
                              pixels: List_Int2,
                              blank: str = "0",
                              plot: str = " ") -> str:
    """
    Returns a string rendering of the supplied canvas coordinated and pixel list.
    Intended to output a graphic raster of ascii chars in an output console
    :param canvas_corner_a: tuple[int, int] - coordinates of canvas first corner
    :param canvas_corner_b: tuple[int, int] - coordinates of canvas second corner
    :param pixels: list[tuple[int, int]] - pixels coordinates to be drawn
    :param blank: str - The char that will be drawn as blank canvas
    :param plot: str - The char that will be drawn as pixel
    :return: str
    """
    str_out: str = ""
    x_inc: int = 1 if canvas_corner_b[0] > canvas_corner_a[0] else -1
    y_inc: int = 1 if canvas_corner_b[1] > canvas_corner_a[1] else -1
    for y in range(canvas_corner_a[1], canvas_corner_b[1], x_inc):
        for x in range(canvas_corner_a[0], canvas_corner_b[0], y_inc):
            if (x, y) in pixels:
                str_out += plot
            else:
                str_out += blank
        str_out += "\n"
    return str_out


"""
Example:
"""
if __name__ == '__main__':
    px0 = cgl_get_pixel_from_uv(0.1, 0.1, 80, 40)
    px1 = cgl_get_pixel_from_uv(0.2, 0.9, 80, 40)
    px2 = cgl_get_pixel_from_uv(0.1, 0.9, 80, 40)
    # pxlist = cgl_line_raster_pixels(px0, px1)
    trilist = cgl_get_triangle_raster_pixels(px0, px1, px2)
    print(cgl_fill_int_range(10, 1))
    output = cgl_get_pixel_plot_string((0, 0), (79, 39), trilist)
    print(output)
