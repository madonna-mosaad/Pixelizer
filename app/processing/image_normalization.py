import numpy as np

class ImageNormalization:
    @staticmethod
    def normalize_image( gray_image):
        """Normalize the image to the range [0, 255]."""
        # Find the minimum and maximum pixel values
        min_val = np.min(gray_image)
        max_val = np.max(gray_image)

        # Create a new image for the normalized values
        normalized_image = np.zeros_like(gray_image, dtype=np.uint8)

        # Apply normalization formula
        if max_val > min_val:  # Avoid division by zero
            normalized_image = ((gray_image - min_val) / (max_val - min_val)) * 255
            normalized_image = normalized_image.astype(np.uint8)  # Convert to uint8 type

        return normalized_image