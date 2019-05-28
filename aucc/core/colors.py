_colors_available = {
    'red': [0x00, 0xFF, 0x00, 0x00],
    'green': [0x00, 0x00, 0xFF, 0x00],
    'blue': [0x00, 0x00, 0x00, 0xFF],
    'teal': [0x00, 0x00, 0xFF, 0xFF],
    'purple': [0x00, 0xFF, 0x00, 0xFF],
    'pink': [0x00, 0xFF, 0x00, 0x77],
    'yellow': [0x00, 0xFF, 0x77, 0x00],
    'white': [0x00, 0xFF, 0xFF, 0xFF],
    'orange': [0x00, 0xFF, 0x1C, 0x00]
}


def get_mono_color_vector(color_name):
    return bytearray(16*_colors_available[color_name])


def get_h_alt_color_vector(color_name_a, color_name_b):
    return bytearray(8*(_colors_available[color_name_a] + _colors_available[color_name_b]))


def get_v_alt_color_vector(color_name_a, color_name_b):
    return bytearray(8*_colors_available[color_name_a] + 8*_colors_available[color_name_b])



