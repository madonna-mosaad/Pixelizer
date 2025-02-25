import cv2
import numpy as np

class AddingNoise:

    @staticmethod
    def add_uniform_noise(image, low=0, high=50):
        noise = np.random.uniform(-high, high, image.shape).astype(np.int16)  # Center around 0
        noisy_image = image.astype(np.int16) + noise
        return np.clip(noisy_image, 0, 255).astype(np.uint8)

    @staticmethod
    def add_gaussian_noise(image, mean=0, sigma=25):
        gaussian = np.random.normal(mean, sigma, image.shape).astype(np.int16)
        noisy_image = image.astype(np.int16) + gaussian
        return np.clip(noisy_image, 0, 255).astype(np.uint8)

    @staticmethod
    def add_salt_and_pepper_noise(image, salt_prob=0.01, pepper_prob=0.01):
        noisy_image = image.copy()
        h, w = image.shape[:2]
        channels = 1 if len(image.shape) == 2 else image.shape[2]

        num_salt = int(salt_prob * h * w * channels)
        num_pepper = int(pepper_prob * h * w * channels)

        # Add salt (white pixels)
        coords = [np.random.randint(0, i, num_salt) for i in image.shape[:2]]
        if channels > 1:
            noisy_image[tuple(coords) + (np.random.randint(0, channels, num_salt),)] = 255
        else:
            noisy_image[tuple(coords)] = 255

        # Add pepper (black pixels)
        coords = [np.random.randint(0, i, num_pepper) for i in image.shape[:2]]
        if channels > 1:
            noisy_image[tuple(coords) + (np.random.randint(0, channels, num_pepper),)] = 0
        else:
            noisy_image[tuple(coords)] = 0

        return noisy_image
