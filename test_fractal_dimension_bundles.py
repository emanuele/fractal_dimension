import numpy as np
from  fractal_dimension import (compute_fractal_dimension,
                                plot_fractal_dimension)
import matplotlib.pyplot as plt
import nibabel as nib


if __name__ == '__main__':
    filename = 'bundles/trk2mask_GTMSK/sub-599469/sub-599469_var-GTMSK_IFO_left.nii.gz'
    # filename = 'bundles/trk2mask_GTMSK/sub-599469/sub-599469_var-GTMSK_IFO_right.nii.gz'
    # filename = 'bundles/trk2mask_GTMSK/sub-599469/sub-599469_var-GTMSK_SLF_I_right.nii.gz'
    # filename = 'bundles/trk2mask_IFOFMSK/sub-599469/sub-599469_var-IFOFMSK_ioff.left.nii.gz'
    image = nib.load(filename).get_data()

    n_steps = 100
    box_side_max = np.min(image.shape) / 3.0
    fractal_dimension, box_side, counts = compute_fractal_dimension(image, n_steps=n_steps, box_side_max=box_side_max)
    print("Fractal dimension = %s" % fractal_dimension)

    plt.ion()
    plot_fractal_dimension(box_side, counts)
