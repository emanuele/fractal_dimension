import numpy as np
from  fractal_dimension import (compute_fractal_dimension,
                                plot_fractal_dimension)
import matplotlib.pyplot as plt
from skimage import io
from skimage.color import rgb2grey


if __name__ == '__main__':
    # filename = 'emanuele_01b.jpg'
    filename = 'Sierpinski_triangle.png'
    image = io.imread(filename)
    image = rgb2grey(image)
    print("Image: %s" % (image.shape,))

    n_steps = 100
    box_size_max = None  # np.min(image.shape) / 3.0
    box_size = np.arange(1, 100)
    fractal_dimension, box_size, counts = compute_fractal_dimension(image,
                                                                    n_steps=n_steps,
                                                                    box_size_max=box_size_max,
                                                                    box_size=box_size)
    print("Fractal dimension = %s" % fractal_dimension)
    if 'ierpinski' in filename:
        print("Expected fractal dimension = %s" % (np.log(3) / np.log(2)))
    
    plt.ion()
    plot_fractal_dimension(box_size, counts)
