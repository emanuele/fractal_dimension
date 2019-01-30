import numpy as np
import matplotlib.pyplot as plt


def my_log(a, base=2.0):
    return np.log(a) / np.log(base)


def compute_fractal_dimension(array, n_steps=10, box_side_min=1.0,
                              box_side_max=None, base=2.0,
                              threshold=0.0, verbose=True):
    pixels = np.array(np.where(array > threshold)).T
    if box_side_max is None:
        box_side_max = np.max(array.shape)

    box_side = np.logspace(my_log(box_side_min, base),
                           my_log(box_side_max, base), num=n_steps,
                           endpoint=False, base=base)
    counts = np.zeros(len(box_side))
    for i, bs in enumerate(box_side):
        bins = [np.arange(0, image_side + bs, bs) for image_side in array.shape]
        H, edges = np.histogramdd(pixels, bins=bins)
        counts[i] = (H > 0).sum()
        if verbose:
            print("Box side=%s , counts=%s" % (bs, counts[i]))

    coefficients = np.polyfit(np.log(box_side), np.log(counts), 1)  # linear regression
    fractal_dimension = -coefficients[0]
    return fractal_dimension, box_side, counts


def plot_fractal_dimension(box_side, counts):
    coefficients = np.polyfit(np.log(box_side), np.log(counts), 1)  # linear regression
    fractal_dimension = -coefficients[0]
    plt.figure()
    plt.loglog(box_side, counts, 'ko')
    plt.loglog(box_side, np.exp(np.polyval(coefficients, np.log(box_side))),
               'r-', label='fractal_dimension=%s' % fractal_dimension)
    plt.xlabel('box_side')
    plt.ylabel('counts')
    plt.axis('tight')
    plt.legend(loc='best', numpoints=1)

