import colorsys


def HLSToRGB(h, l, s):
    (r, g, b) = colorsys.hls_to_rgb(h, l, s)
    return (int(255 * r), int(255 * g), int(255 * b))


def getDistinctColors(n, luminance=0.5, saturation=1., to_hex=True):
    huePartition = 1.0 / (n + 1)
    rgb_colors = [HLSToRGB(huePartition * hue_value, luminance, saturation) for hue_value in range(0, n)]
    if to_hex:
        return [RGBtoHex(*rgb) for rgb in rgb_colors]
    else:
        return rgb_colors


def RGBtoHex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"



if __name__ == "__main__":
    print(getDistinctColors(2))
    print(getDistinctColors(3))
    print(getDistinctColors(10))
