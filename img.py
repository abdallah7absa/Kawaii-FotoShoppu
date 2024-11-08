
import cv2
import numpy as np

def rgb_to_gray_pixel_processing(image_path, output_path, r1, r2, r3):

    image = cv2.imread(image_path)
    
    height, width, _ = image.shape
    
    gray_image = np.zeros((height, width), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):
            r, g, b = image[y, x]
            gray = int(r1 * r + r2 * g + r3 * b)
            gray_image[y, x] = gray
    
    # cv2.imshow('gray Image', gray_image)

    cv2.imwrite(output_path, gray_image)

def rgb_to_binary_pixel_processing(image_path, output_path, r1, r2, r3, threshold):

    image = cv2.imread(image_path)
    
    height, width, _ = image.shape
    
    binary_image = np.zeros((height, width), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):
            r, g, b = image[y, x]
            gray = 0.299 * r + 0.587 * g + 0.114 * b
            binary_image[y, x] = 255 if gray > threshold else 0
    
    # cv2.imshow('Original Image', image)
    # cv2.imshow('Binary Image', binary_image)
    
    cv2.imwrite(output_path, binary_image)

def brightness_operations(image_path, output_path, op, value):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    height, width = image.shape
    
    new_image = np.zeros((height, width), dtype=np.uint8)
    
    if op == "Add value":
        height, width = image.shape
        for y in range(height):
            for x in range(width):
                new_value = image[y, x] + value
                image[y, x] = np.clip(new_value, 0, 255)
        new_image = image
    elif op == "Subtract value":
        height, width = image.shape
        for y in range(height):
            for x in range(width):
                new_value = image[y, x] - value
                image[y, x] = np.clip(new_value, 0, 255)
        new_image = image
    elif op == "Multiply value":
        height, width = image.shape
        for y in range(height):
            for x in range(width):
                new_value = image[y, x] * value
                image[y, x] = np.clip(new_value, 0, 255)
        new_image = image
    elif op == "Divide value":
        if value == 0:
            raise ValueError("Division by zero is not allowed.")
        height, width = image.shape
        for y in range(height):
            for x in range(width):
                new_value = image[y, x] / value
                image[y, x] = np.clip(new_value, 0, 255)
        new_image = image

            
    # cv2.imshow(f'new brightness image {op}', new_image)
    
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    cv2.imwrite(output_path, new_image)

def gamma_correction(image_path, output_path, gamma):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    inv_gamma = gamma
    gamma_corrected = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    gamma_corrected = cv2.LUT(image, gamma_corrected)
    cv2.imwrite(output_path, gamma_corrected)

def log_transform(image_path, output_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)    
    # Avoid divide by zero by adding a small constant (epsilon)
    epsilon = 1e-5
    image = image + epsilon
    c = 255 / np.log(1 + np.max(image))
    log_image = c * np.log(image + 1)
    log_image = np.clip(log_image, 0, 255)
    log_image = np.array(log_image, dtype=np.uint8)    
    cv2.imwrite(output_path, log_image)

def inverse_log_transform(image_path, output_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Avoid divide by zero by adding a small constant (epsilon)
    epsilon = 1e-5
    image = image + epsilon
    c = 255 / np.log(1 + np.max(image))
    inverse_log_image = np.exp(image / c) - 1
    inverse_log_image = np.clip(inverse_log_image, 0, 255)
    inverse_log_image = np.array(inverse_log_image, dtype=np.uint8)
    cv2.imwrite(output_path, inverse_log_image)

def complement(image_path, output_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    complement_image = 255 - image
    cv2.imwrite(output_path, complement_image)

def calculate_histogram(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    histogram = np.zeros(256, dtype=int)
    
    for row in image:
        for pixel in row:
            histogram[pixel] += 1
            
    return histogram

def contrast_stretching(image_path, l, r, output_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    a = np.min(image)
    b = np.max(image)
    
    stretched_image = ((image - a) / (b - a) * (r-l)+l).astype(np.uint8)
    
    cv2.imwrite(output_path, stretched_image)

def histogram_equalization(image_path, output_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    histogram = calculate_histogram(image_path)

    cdf = histogram.cumsum()

    cdf_normalized = cdf * (255 / cdf[-1])

    equalized_image = np.interp(image.flatten(), np.arange(256), cdf_normalized)

    equalized_image = equalized_image.reshape(image.shape).astype(np.uint8)

    cv2.imwrite(output_path, equalized_image)


if __name__ == "__main__":
    rgb_img = "assets/img.jpg"
    gray_image = "img2.jpg"
    bin_image = "img3.jpg"

    rgb_to_gray_pixel_processing(rgb_img, gray_image, 0.299, 0.587, 0.114)
    rgb_to_binary_pixel_processing(rgb_img, bin_image, 0.299, 0.587, 0.114, 128)
    brightness_operations(gray_image, '/', 2)
    brightness_operations(gray_image, '+', 128)
    brightness_operations(gray_image, '-', 128)
    brightness_operations(gray_image, '*', 2)

