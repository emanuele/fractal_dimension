import numpy as np
from  fractal_dimension import (compute_fractal_dimension,
                                plot_fractal_dimension)
import matplotlib.pyplot as plt
import nibabel as nib


if __name__ == '__main__':
    subject = '896778'  # '599469'  # 
    hemisphere = 'left'  # 'right'
    filename = 'bundles/trk2mask_GTMSK/sub-%s/sub-%s_var-GTMSK_IFO_%s.nii.gz' % (subject, subject, hemisphere)
    # filename = 'bundles/trk2mask_IFOFMSK/sub-%s/sub-%s_var-IFOFMSK_ioff.%s.nii.gz' % (subject, subject, hemisphere)
    # filename = 'bundles/bundle_masks_IFOF/sub-%s/IFO_%s.nii.gz' % (subject, hemisphere)
    print("Loading %s" % filename)
    image = nib.load(filename).get_data()

    n_steps = 100
    box_size_max = None # 5.0 # np.min(image.shape) / 3.0
    box_size = np.arange(1, 15)
    fractal_dimension, box_size, counts = compute_fractal_dimension(image,
                                                                    n_steps=n_steps,
                                                                    box_size_max=box_size_max,
                                                                    box_size=box_size)
    print("Fractal dimension = %s" % fractal_dimension)

    plt.ion()
    plot_fractal_dimension(box_size, counts)
