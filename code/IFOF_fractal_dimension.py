import numpy as np
from  fractal_dimension import (compute_fractal_dimension,
                                plot_fractal_dimension)
import nibabel as nib
from glob import glob
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel


def load_compute(filename):
    image = nib.load(filename).get_data()
    box_side_max = np.min(image.shape) / 3.0
    fractal_dimension, box_side, counts = compute_fractal_dimension(image, n_steps=n_steps, box_side_max=box_side_max, verbose=False)
    return fractal_dimension


if __name__ == '__main__':
    segmented_by_tractseg = False

    if segmented_by_tractseg:
        subjects_path = glob('bundles/bundle_masks_IFOF/sub-*')  # segmented by Tractseg
    else:
        subjects_path = glob('bundles/trk2mask_IFOFMSK/sub-*')  # manually segmented by Pietro

    subjects_id = sorted([sp[-6:] for sp in subjects_path])
    if segmented_by_tractseg:
        subjects_id.remove('991267')  # outlier: TractSeg fails in segmenting

    template_gt_tractseg = 'bundles/trk2mask_GTMSK/sub-%s/sub-%s_var-GTMSK_IFO_left.nii.gz'  # Groud Truth TractSeg
    template_gt_pietro = 'bundles/trk2mask_IFOFMSK/sub-%s/sub-%s_var-IFOFMSK_ioff.left.nii.gz'  # GRound Truth Pietro
    if segmented_by_tractseg:
        template_tractseg = 'bundles/bundle_masks_IFOF/sub-%s/IFO_left.nii.gz'  # Segmented by TractSeg

    n_steps = 50
    fd_gt_tractseg = np.zeros(len(subjects_id))
    fd_gt_pietro = np.zeros(len(subjects_id))
    if segmented_by_tractseg:
        fd_tractseg = np.zeros(len(subjects_id))

    for i, sid in enumerate(subjects_id):
        filename_gt_tractseg = template_gt_tractseg % (sid, sid)
        fd_gt_tractseg[i] = load_compute(filename_gt_tractseg)
        print("%s - FD = %s" % (filename_gt_tractseg, fd_gt_tractseg[i]))

        filename_gt_pietro = template_gt_pietro % (sid, sid)
        fd_gt_pietro[i] = load_compute(filename_gt_pietro)
        print("%s - FD = %s" % (filename_gt_pietro, fd_gt_pietro[i]))

        if segmented_by_tractseg:
            filename_tractseg = template_tractseg % (sid)
            fd_tractseg[i] = load_compute(filename_tractseg)
            print("%s - FD = %s" % (filename_tractseg, fd_tractseg[i]))

    print("")
    print("Mean/Std Fractal Dimension for GT Tractseg: %s / %s" % (fd_gt_tractseg.mean(), fd_gt_tractseg.std()))
    print("Mean/Std Fractal Dimension for GT Pietro: %s / %s" % (fd_gt_pietro.mean(), fd_gt_pietro.std()))
    if segmented_by_tractseg:
        print("Mean/Std Fractal Dimension for Tractseg: %s / %s" % (fd_tractseg.mean(), fd_tractseg.std()))
    t, p_value = ttest_rel(fd_gt_tractseg, fd_gt_pietro)
    print("Paired Two-sample t-test: p-value=%s" % p_value)    

    plt.ion()
    plt.figure()
    n_bins = 20
    if segmented_by_tractseg:
        tmp = np.concatenate([fd_gt_tractseg, fd_gt_pietro, fd_tractseg])
    else:
        tmp = np.concatenate([fd_gt_tractseg, fd_gt_pietro])

    bins = np.linspace(tmp.min(), tmp.max(), n_bins)
    plt.hist(fd_gt_tractseg, bins=bins, color='r', label='GT Tractseg', alpha=0.5)
    plt.hist(fd_gt_pietro, bins=bins, color='b', label='GT Pietro', alpha=0.5)
    if segmented_by_tractseg:
        plt.hist(fd_tractseg, bins=bins, color='g', label='Tractseg', alpha=0.5)

    plt.legend(loc='best', numpoints=1)
    plt.xlabel('Fractal Dimension')
