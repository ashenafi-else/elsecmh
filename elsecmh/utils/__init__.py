def srgb_to_linearrgb(c):
    """
    Transform the sRGB values into linear
    https://en.wikipedia.org/wiki/SRGB

    Parameters
    ----------
    c: float
        Normalized value from sRGB vector. Can be from 0 to 1.

    Returns
    -------
    float
        Converted to linear rgb value.
    """
    if c < 0.04045:
        return 0 if c < 0 else c * (1 / 12.92)
    return pow((c + 0.055) * (1 / 1.055), 2.4)


def rgb_to_srgb(a, b, c):
    return (srgb_to_linearrgb(v) for v in (a, b, c))


def hex_to_rgb(value):
    """
    Convert HEX color representation to RGB if it possible else return default value

    Parameters
    ----------
    value: string
        Color in HEX format.

    Returns
    -------
    tuple of float
        RGB color vector
    """
    value = value.lstrip('#')
    lv = len(value)
    fin = list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    r = srgb_to_linearrgb(fin[0] / 255)
    g = srgb_to_linearrgb(fin[1] / 255)
    b = srgb_to_linearrgb(fin[2] / 255)
    alpha = 1.0

    return r, g, b, alpha
