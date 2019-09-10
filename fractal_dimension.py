import numpy as np
import matplotlib.pyplot as plt


def my_log(a, base=2.0):
    return np.log(a) / np.log(base)


def compute_fractal_dimension(array, n_steps=10, box_size_min=1.0,
                              box_size_max=None, base=2.0,
                              threshold=0.0, box_size=None,
                              verbose=True):
    pixels = np.array(np.where(array > threshold)).T
    if box_size_max is None:
        box_size_max = np.max(array.shape)

    if box_size is None:
        box_size = np.logspace(my_log(box_size_min, base),
                               my_log(box_size_max, base),
                               num=n_steps, endpoint=False, base=base)

    counts = np.zeros(len(box_size))
    for i, bs in enumerate(box_size):
        bins = [np.arange(0, image_side + bs, bs) for image_side in array.shape]
        H, edges = np.histogramdd(pixels, bins=bins)
        counts[i] = (H > 0).sum()
        if verbose:
            print("Box side=%s , counts=%s" % (bs, counts[i]))

    if (counts < 1).any():
        fractal_dimension = 0.0
    else:
        # linear regression:
        coefficients = np.polyfit(np.log(box_size), np.log(counts), 1)
        fractal_dimension = -coefficients[0]

    return fractal_dimension, box_size, counts


def plot_fractal_dimension(box_size, counts):
    if (counts >= 1).all():
        # linear regression:
        coefficients = np.polyfit(np.log(box_size), np.log(counts), 1)
        fractal_dimension = -coefficients[0]
        plt.figure()
        plt.loglog(box_size, counts, 'ko')
        plt.loglog(box_size, np.exp(np.polyval(coefficients, np.log(box_size))),
                   'r-', label='fractal_dimension=%s' % fractal_dimension)
        plt.xlabel('box_size')
        plt.ylabel('counts')
        plt.axis('tight')
        plt.legend(loc='best', numpoints=1)
    else:
        print("Cannot plot when counts is zero")
