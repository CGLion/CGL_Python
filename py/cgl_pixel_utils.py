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


def cgl_get_integer_line_pixels(x0, y0, x1, y1):
    """
    Returns a list of integer tuples
    representing 2D coordinated of the pixels plotting a line from point 0 to point 1
    as defined by the supplied x0, y0, x1, y1 integer arguments.
    This function is based on the Bresenham line algorithm as it's explained in wikipedia:
    https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    And is expended to handle the cases where teh line slope is larger than 1 i.e delta Y is larger than delta X,
    and also cases where the the line is drawn "backwards" for a large X or Y to a small X or Y.
    :param x0: Int - the x coordinate of point 0
    :param y0: Int - the y coordinate of point 0
    :param x1: Int - the x coordinate of point 1
    :param y1: Int - the y coordinate of point 1
    :return: list of integer tuples
    """
    # store line coords in 2d array:
    ln = [[x0, y0],
          [x1, y1]]
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
    inc = 1 if d[1-mx] >= 0 else -1
    # Make delta values absolute
    d[0] = abs(d[0])
    d[1] = abs(d[1])
    # Set init derivation:
    di = (2 * d[1-mx]) - d[mx]
    # Set secondary axis start value:
    sec = ln[0][1-mx]
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
        di = di + (2 * d[1-mx])
    # Return output list:
    return line_px


def cgl_get_pixel_plot_string(canvas_corner_a, canvas_corner_b, pixels, blank="0", plot=" "):
    """
    Returns a string rendering of the supplied canvas coordinated and pixel list.
    Intended to output a graphic easter in an ascii output console
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
px0 = cgl_get_pixel_from_uv(0.4, 0.1, 80, 40)
px1 = cgl_get_pixel_from_uv(0.6, 0.9, 80, 40)
pxlist = cgl_get_integer_line_pixels(px0[0], px0[1], px1[0], px1[1])
output = cgl_get_pixel_plot_string((0, 0), (79, 39), pxlist)
print(output)
