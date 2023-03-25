
def min_max_scale(data):
    data_min = 0
    data_max = 443
    scaled_data = (data - data_min) / (data_max - data_min)
    return scaled_data