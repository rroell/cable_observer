import cv2 
import matplotlib.pyplot as plt
from time import perf_counter

from mask_segmentation import MaskSegmentation
from path_processing import PathProcessing
from spline_mask import SplineMask


class CableObserver():
    def __init__(self, is_masked):
        t1 = perf_counter()
        self.segmentation = MaskSegmentation(is_masked=is_masked)
        t2 = perf_counter()
        self.paths = PathProcessing()
        t3 = perf_counter()
        self.spline_mask = SplineMask()
        t4 = perf_counter()
        print(f"{(t2-t1)*1000}, {(t3-t2)*1000}, {(t4-t3)*1000} -> {(t4-t1)*1000} [ms]")

    def exec(self, input_image):
        # mask segmentation
        mask_image = self.segmentation.exec(input_image)

        # paths processing
        spline_coords, spline_params = self.paths.exec(mask_image=mask_image, paths_ends=self.segmentation.paths_ends)

        # math repr (spline) to image
        spline_mask = self.spline_mask.exec(splines=spline_coords, shape=input_image.shape)

        return spline_mask
    

if __name__ == "__main__":
    img_path = "imgs/006.png"
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    p = CableObserver(is_masked=True)
    output_mask = p.exec(input_image=img)
    plt.imshow(output_mask)
    plt.axis("off")
    plt.tight_layout(pad=0.1)
    plt.show()
