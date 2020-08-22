"""
Functions for image / pixel processing
Written by Oded Erell - CG-Lion Studio (c)2020
"""


def cgl_get_pixel_from_uv(u, v, w, h):
    """
    Returns an Tuple containing 2D integer coordinates
    of the pixel corresponding to the supplied UV coordinates and image width and height in pixels.
    The supplied u and v arguments are clamped to a 0.0 - 1.0 range.
    :param u: Float - [0.0 - 1.0] - Supplied U coordinate
    :param v: Float - [0.0 - 1.0] - Supplied V coordinate
    :param w: Int - The image width in pixels
    :param h: Int - The image height in pixels
    :return: Tuple containing integers
    """
    # Clamp the UV values
    u = max(min(u, 1.0), 0.0)
    v = max(min(v, 1.0), 0.0)
    # Calculate and return pixel coordinates:
    return int(round(u * (w - 1))), int(round(v * (h - 1)))


def cgl_get_pixel_uv(x, y, w, h):
    """
    Return a tuple containing floats representing UV coordinates of the center of the supplied pixel.
    :param x: Int - the pixel x coordinate
    :param y: Int - the pixel y coordinate
    :param w: Int - The image width
    :param h: Int - The image Height
    :return: Tuple containing Floats
    """
    px_u_step = 1.0 / w
    px_v_step = 1.0 / h
    x = int(max(min(x, w - 1), 0))
    y = int(max(min(y, h - 1), 0))
    return (x * px_u_step) + (px_u_step * 0.5), (y * px_v_step) + (px_v_step * 0.5)


def cgl_line_raster_pixels(p0, p1):
    """
    Returns a list of integer tuples
    representing 2D coordinated of the pixels plotting a line from point 0 to point 1
    as defined by the supplied p0, p1 integer tuple arguments.
    This function is based on the Bresenham line algorithm as it's explained in wikipedia:
    https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    And is expended to handle the cases where teh line slope is larger than 1 i.e delta Y is larger than delta X,
    and also cases where the the line is drawn "backwards" for a large X or Y to a small X or Y.
    :param p0: Tuple - Int - the x,y coordinate of point 0
    :param p1: Tuple - Int - the x,y coordinate of point 1
    :return: list of integer tuples
    """
    # store line coords in 2d array:
    ln = [[p0[0], p0[1]],
          [p1[0], p1[1]]]
    # Make sure input values ar integers:
    for i in range(2):
        for j in range(2):
            ln[i][j] = int(ln[i][j])
    # Init list of line pixel coordinates - Int tuples
    line_px = []
    # Get x y delta
    d = [ln[1][0] - ln[0][0],
         ln[1][1] - ln[0][1]]
    # Set main iteration axis:
    mx = 0 if abs(d[0]) > abs(d[1]) else 1
    # Set if secondary increment is positive or negative
    inc = 1 if d[1 - mx] >= 0 else -1
    # Make delta values absolute
    d[0] = abs(d[0])
    d[1] = abs(d[1])
    # Set init derivation:
    di = (2 * d[1 - mx]) - d[mx]
    # Set secondary axis start value:
    sec = ln[0][1 - mx]
    # Generate main axis value range:
    mrange = range(ln[0][mx], ln[1][mx] + 1) if ln[0][mx] < ln[1][mx] else range(ln[0][mx], ln[1][mx] - 1, -1)
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


def cgl_get_triangle_lines_raster_pixels(p0, p1, p2):
    """
    Returns a list of tuples representing the raster pixels of the contour of triangle p0, p1, p2
    :param p0: tuple - integer - integer x, y coordinates of pixel 0 of the triangle
    :param p1: tuple - integer - integer x, y coordinates of pixel 1 of the triangle
    :param p2: tuple - integer - integer x, y coordinates of pixel 2 of the triangle
    :return: list of integer tuples
    """
    points = [p0, p1, p2]
    tri_px = []
    for i in range(3):
        tri_px += (cgl_line_raster_pixels(points[i], points[(i + 1) % 3]))[1:]
    return tri_px


def cgl_get_triangle_raster_pixels(p0, p1, p2, lines=True):
    """
    Returns a list of tuples representing the raster pixels of the filled area of triangle p0, p1, p2 (without contours)
    :param p0: tuple - integer - integer x, y coordinates of pixel 0 of the triangle
    :param p1: tuple - integer - integer x, y coordinates of pixel 1 of the triangle
    :param p2: tuple - integer - integer x, y coordinates of pixel 2 of the triangle
    :param lines: bool - when True, the output list will include the triangle contours
    :return: list of integer tuples
    """
    points = [p0, p1, p2]
    sorted_y = sorted(points, key=lambda x: x[1])
    line_a = cgl_line_raster_pixels(sorted_y[0], sorted_y[2])
    line_b = cgl_line_raster_pixels(sorted_y[0], sorted_y[1])
    line_c = cgl_line_raster_pixels(sorted_y[1], sorted_y[2])
    tri_fill = []
    y_val = line_a[0][1]
    for i in list(range(len(line_a)))[1:-1]:
        new_y_val = line_a[i][1]
        if new_y_val != y_val:
            sec_line = line_b if new_y_val <= line_b[-1][1] else line_c
            sec_index = list(zip(*sec_line))[1].index(new_y_val)
            x_vals = list(range(line_a[i][0], sec_line[sec_index][0]))[1:]
            y_vals = [new_y_val] * len(x_vals)
            tri_fill += zip(x_vals, y_vals)
            y_val = new_y_val
    if lines:
        outlist = tri_fill + line_a[1:] + line_b[1:] + line_c[1:]
    else:
        outlist = tri_fill
    return outlist


def cgl_get_pixel_plot_string(canvas_corner_a, canvas_corner_b, pixels, blank="0", plot=" "):
    """
    Returns a string rendering of the supplied canvas coordinated and pixel list.
    Intended to output a graphic raster of ascii chars in an output console
    :param canvas_corner_a: Int Tuple of canvas first corner
    :param canvas_corner_b: Int Tuple of canvas second corner
    :param pixels: List of Int Tuple objects representing pixel coordinates to be drawn
    :param blank: The char that will be drawn as blank canvas
    :param plot: The char that will be drawn as pixel
    :return: str
    """
    str_out = ""
    x_inc = 1 if canvas_corner_b[0] > canvas_corner_a[0] else -1
    y_inc = 1 if canvas_corner_b[1] > canvas_corner_a[1] else -1
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
px0 = cgl_get_pixel_from_uv(0.1, 0.1, 80, 40)
px1 = cgl_get_pixel_from_uv(0.6, 0.1, 80, 40)
px2 = cgl_get_pixel_from_uv(0.1, 0.6, 80, 40)
# pxlist = cgl_line_raster_pixels(px0, px1)
trilist = cgl_get_triangle_raster_pixels(px0, px1, px2)
output = cgl_get_pixel_plot_string((0, 0), (79, 39), trilist)
print(output)
