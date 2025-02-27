import numpy as np

class EqualizeHistogram:
    @staticmethod
    def equalizeHist(image):
        # Ensure the image is in grayscale
        if len(image.shape) != 2:
            raise ValueError("Input image must be a grayscale image.")

        # Calculate the histogram
        hist, bins = np.histogram(image.flatten(), 256, [0, 256])

        # Calculate the cumulative distribution function (CDF)
        cdf = hist.cumsum()

        # Normalize the CDF
        cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
        cdf_normalized = np.ma.filled(cdf_normalized, 0).astype('uint8')

        # Map the original image pixels to equalized values
        equalized_image = cdf_normalized[image]

        return equalized_image