import numpy as np
from  fractal_dimension import (compute_fractal_dimension,
                                plot_fractal_dimension)
import matplotlib.pyplot as plt


if __name__ == '__main__':
    side = 200
    fill = 'N lines'  # '2d box'  # '3 lines'  # '3d box'  #
    N = 20
    mid = int(side / 2)
    quarter = int(side / 4)
    image = np.zeros((side, side, side))
    if fill == '3 lines':
        image[:, mid, mid] = 1
        image[:, mid-20, mid-20] = 1
        image[:, mid+20, mid+20] = 1
    elif fill == 'N lines':
        i = np.random.randint(side, size=N)
        j = np.random.randint(side, size=N)
        image[:, i, j] = 1
    elif fill == '2d box':
        image[quarter:mid+quarter, quarter:mid+quarter, mid] = 1
    elif fill == '3d box':
        image[quarter:mid+quarter, quarter:mid+quarter, quarter:mid+quarter] = 1
    else:
        pass

    print("Image: %s" % (image.shape,))

    n_steps = 100
    box_size_max = None  # np.min(image.shape) / 3.0
    box_size = np.linspace(1, 5, 100)
    fractal_dimension, box_size, counts = compute_fractal_dimension(image,
                                                                    n_steps=n_steps,
                                                                    box_size_max=box_size_max,
                                                                    box_size=box_size)
    print("Fractal dimension = %s" % fractal_dimension)
    plt.ion()
    plot_fractal_dimension(box_size, counts)
