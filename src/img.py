
import cv2
import numpy as np
import random

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
def gray_to_binary_pixel_processing(image_path, output_path, threshold):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    height, width = image.shape

    binary_image = np.zeros((height, width), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):
            gray = image[y, x]
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
def salt_and_pepper_noise(image_path, output_path, amount, salt_vs_pepper=0.5):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    noisy_image = image.copy()
    total_pixels = image.size
    num_salt = int(amount * total_pixels * salt_vs_pepper)
    num_pepper = int(amount * total_pixels * (1 - salt_vs_pepper))

    for _ in range(num_salt):
        x = random.randint(0, image.shape[0] - 1)
        y = random.randint(0, image.shape[1] - 1)
        noisy_image[x, y] = 255

    for _ in range(num_pepper):
        x = random.randint(0, image.shape[0] - 1)
        y = random.randint(0, image.shape[1] - 1)
        noisy_image[x, y] = 0

    cv2.imwrite(output_path, noisy_image)
def uniform_noise(image_path, output_path, noise_range):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    noisy_image = np.zeros_like(image, dtype=np.uint8)
    
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            noise = random.uniform(-noise_range, noise_range)
            noisy_value = image[i, j] + noise
            noisy_image[i, j] = max(0, min(255, int(noisy_value)))

    cv2.imwrite(output_path, noisy_image)
def gaussian_noise(image_path, output_path, mean, std_dev):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    noisy_image = np.zeros_like(image, dtype=np.uint8)
    
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            noise = random.gauss(mean, std_dev)
            noisy_value = image[i, j] + noise
            noisy_image[i, j] = max(0, min(255, int(noisy_value)))

    cv2.imwrite(output_path, noisy_image)
def get_neighbors(image, x, y, ksize):
    neighbors = []
    for i in range(-(ksize // 2), (ksize // 2) + 1):
        for j in range(-(ksize // 2), (ksize // 2) + 1):
            ni, nj = x + i, y + j
            if 0 <= ni < image.shape[0] and 0 <= nj < image.shape[1]:
                neighbors.append(image[ni, nj])
    return neighbors
def min_filter(image_path, output_path, ksize):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    output = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            neighbors = get_neighbors(image, i, j, ksize)
            output[i, j] = min(neighbors)

    cv2.imwrite(output_path, output)
def max_filter(image_path, output_path, ksize):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    output = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            neighbors = get_neighbors(image, i, j, ksize)
            output[i, j] = max(neighbors)

    cv2.imwrite(output_path, output)
def median_filter(image_path, output_path, ksize):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    output = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            neighbors = get_neighbors(image, i, j, ksize)
            output[i, j] = sorted(neighbors)[len(neighbors) // 2]

    cv2.imwrite(output_path, output)
def midpoint_filter(image_path, output_path, ksize):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    output = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            neighbors = get_neighbors(image, i, j, ksize)
            min_val = int(min(neighbors))
            max_val = int(max(neighbors))
            output[i, j] = (min_val + max_val) // 2

    cv2.imwrite(output_path, output)
def fourier_transform(image_path, output_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Image not found or unable to read")

    image_float = np.float32(image)

    dft = cv2.dft(image_float, flags=cv2.DFT_COMPLEX_OUTPUT)

    dft_shifted = np.fft.fftshift(dft)

    magnitude, angle = cv2.cartToPolar(dft_shifted[:, :, 0], dft_shifted[:, :, 1])

    magnitude += 1  # To avoid log(0)
    log_magnitude = np.log(magnitude)

    log_magnitude = np.uint8(255 * (log_magnitude - np.min(log_magnitude)) / (np.max(log_magnitude) - np.min(log_magnitude)))

    cv2.imwrite(output_path, log_magnitude)

    return dft_shifted, magnitude, angle
def inverse_fourier_transform(dft_shifted, magnitude, angle, output_path):
    real, imaginary = cv2.polarToCart(magnitude, angle)

    complex_dft = np.stack((real, imaginary), axis=-1)

    complex_dft_shifted_back = np.fft.ifftshift(complex_dft)

    idft = cv2.idft(complex_dft_shifted_back)

    restored_image = cv2.magnitude(idft[:, :, 0], idft[:, :, 1])

    restored_image = cv2.normalize(restored_image, None, 0, 255, cv2.NORM_MINMAX)

    restored_image = np.uint8(np.clip(restored_image, 0, 255))

    cv2.imwrite(output_path, restored_image)
def ideal_low_pass_filter(image_path, output_path, cutoff_radius):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    
    mask = np.zeros((rows, cols), dtype=np.float32)
    for i in range(rows):
        for j in range(cols):
            if (i - crow) ** 2 + (j - ccol) ** 2 <= cutoff_radius ** 2:
                mask[i, j] = 1
    
    fshift_filtered = fshift * mask
    
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    cv2.imwrite(output_path, img_back)
def ideal_high_pass_filter(image_path, output_path, cutoff_radius):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    
    mask = np.ones((rows, cols), dtype=np.float32)
    for i in range(rows):
        for j in range(cols):
            if (i - crow) ** 2 + (j - ccol) ** 2 <= cutoff_radius ** 2:
                mask[i, j] = 0
    
    fshift_filtered = fshift * mask
    
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    cv2.imwrite(output_path, img_back)
def gaussian_low_pass_filter(image_path, output_path, cutoff_radius):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    
    mask = np.zeros((rows, cols), dtype=np.float32)
    for i in range(rows):
        for j in range(cols):
            d = np.sqrt((i - crow) ** 2 + (j - ccol) ** 2)
            mask[i, j] = np.exp(-(d ** 2) / (2 * (cutoff_radius ** 2)))
    
    fshift_filtered = fshift * mask
    
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    cv2.imwrite(output_path, img_back)
def gaussian_high_pass_filter(image_path, output_path, cutoff_radius):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    
    mask = np.ones((rows, cols), dtype=np.float32)
    for i in range(rows):
        for j in range(cols):
            d = np.sqrt((i - crow) ** 2 + (j - ccol) ** 2)
            mask[i, j] = 1 - np.exp(-(d ** 2) / (2 * (cutoff_radius ** 2)))
    
    fshift_filtered = fshift * mask
    
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    cv2.imwrite(output_path, img_back)
def butterworth_low_pass_filter(image_path, output_path, cutoff_radius, order=2):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    
    mask = np.zeros((rows, cols), dtype=np.float32)
    for i in range(rows):
        for j in range(cols):
            D = np.sqrt((i - crow) ** 2 + (j - ccol) ** 2)
            mask[i, j] = 1 / (1 + (D / cutoff_radius) ** (2 * order))
    
    fshift_filtered = fshift * mask
    
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    cv2.imwrite(output_path, img_back)
def butterworth_high_pass_filter(image_path, output_path, cutoff_radius, order=2):

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    
    mask = np.ones((rows, cols), dtype=np.float32)
    for i in range(rows):
        for j in range(cols):
            D = np.sqrt((i - crow) ** 2 + (j - ccol) ** 2)
            mask[i, j] = 1 - 1 / (1 + (D / cutoff_radius) ** (2 * order))
    
    fshift_filtered = fshift * mask
    
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    cv2.imwrite(output_path, img_back)
def blurring_mean_filter(image_path, output_path, kernel_size):
    image = cv2.imread(image_path)
    i_filter=np.ones(kernel_size, dtype=np.float32) / (kernel_size[0] * kernel_size[1])
    if len(image.shape) == 3:
        height, width, channels = image.shape
        blurred_image = np.zeros_like(image, dtype=np.uint8)
    else:
        height, width = image.shape
        blurred_image = np.zeros_like(image, dtype=np.uint8)
    pad_h, pad_w = kernel_size[0] // 2, kernel_size[1] // 2
    if len(image.shape) == 3:
        padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    else:
        padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    for i in range(height):
        for j in range(width):
            if len(image.shape) == 3: 
                for l in range(channels):
                    region = padded_image[i:i + kernel_size[0], j:j + kernel_size[1], l]
                    blurred_image[i, j, l] = np.sum(region * i_filter)
            else:
                region = padded_image[i:i + kernel_size[0], j:j + kernel_size[1]]
                blurred_image[i, j] = np.sum(region * i_filter)
    cv2.imwrite(output_path, blurred_image)
def blurring_weight_filter(image_path, output_path):
    image = cv2.imread(image_path)
    kernel=np.array([[125, 150, 125],
    [150, 200, 150],
    [125, 150, 125]],dtype=np.float32)
    i_filter=  kernel/np.sum(kernel)
    if len(image.shape) == 3:  
        height, width, channels = image.shape
        blurred_image = np.zeros_like(image, dtype=np.uint8)
    else:  
        height, width = image.shape
        blurred_image = np.zeros_like(image, dtype=np.uint8)
    k_height, k_width = kernel.shape
    pad_h, pad_w = k_height // 2, k_width // 2
    pad_h, pad_w = k_height // 2, k_width // 2
    if len(image.shape) == 3:
        padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    else:
        padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    for i in range(height):
        for j in range(width):
            if len(image.shape) == 3: 
                for l in range(channels):
                    region = padded_image[i:i + k_height, j:j + k_width, l]
                    blurred_image[i, j, l] = np.sum(region * i_filter)
            else:
                region = padded_image[i:i + k_height, j:j + k_width]
                blurred_image[i, j] = np.sum(region * i_filter)
    cv2.imwrite(output_path, blurred_image)
def horizontal_edge_detection(image_path, output_path):
    image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    vertical_kernel = np.array([
        [ 1,  2,  1],
        [ 0,  0,  0],
        [-1, -2, -1]
    ], dtype=np.float32)
    img_height, img_width = image.shape
    kernel_height, kernel_width = vertical_kernel.shape
    pad_h, pad_w = kernel_height // 2, kernel_width // 2
    padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    edge_image = np.zeros_like(image, dtype=np.float32)
    for i in range(img_height):
        for j in range(img_width):
            region = padded_image[i:i + kernel_height, j:j + kernel_width]
            edge_value = np.sum(region * vertical_kernel)
            edge_image[i, j] = edge_value
    edge_image = np.abs(edge_image)  
    edge_image = (edge_image / edge_image.max()) * 255
    horizontal_edge_image = edge_image.astype(np.uint8)
    cv2.imwrite(output_path, horizontal_edge_image)
def vertical_edge_detection(image_path, output_path):
    image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    vertical_kernel = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float32)
    img_height, img_width = image.shape
    kernel_height, kernel_width = vertical_kernel.shape
    pad_h, pad_w = kernel_height // 2, kernel_width // 2
    padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    edge_image = np.zeros_like(image, dtype=np.float32)
    for i in range(img_height):
        for j in range(img_width):
            region = padded_image[i:i + kernel_height, j:j + kernel_width]
            edge_value = np.sum(region * vertical_kernel)
            edge_image[i, j] = edge_value
    edge_image = np.abs(edge_image)  
    edge_image = (edge_image / edge_image.max()) * 255
    vertical_edge_image = edge_image.astype(np.uint8)
    
    cv2.imwrite(output_path, vertical_edge_image)
def point_edge_detection(image_path, output_path):
    image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    point_kernel = np.array([
        [ 0, -1,  0],
        [-1,  4, -1],
        [ 0, -1,  0]
    ], dtype=np.float32)
    img_height, img_width = image.shape
    kernel_height, kernel_width = point_kernel.shape
    pad_h, pad_w = kernel_height // 2, kernel_width // 2
    padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    edge_image = np.zeros_like(image, dtype=np.float32)
    for i in range(img_height):
        for j in range(img_width):
            region = padded_image[i:i + kernel_height, j:j + kernel_width]
            edge_value = np.sum(region * point_kernel)
            edge_image[i, j] = edge_value
    edge_image = np.abs(edge_image)  
    edge_image = (edge_image / edge_image.max()) * 255
    point_edge_image = edge_image.astype(np.uint8) 
    cv2.imwrite(output_path, point_edge_image)
def diagonal_left_edge_detection(image_path, output_path):
    image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    diagonal_left_kernel = np.array([
        [ 0, -1,  -2],
        [1,  0, -1],
        [ 2, 1,  0]
    ], dtype=np.float32)
    img_height, img_width = image.shape
    kernel_height, kernel_width = diagonal_left_kernel.shape
    pad_h, pad_w = kernel_height // 2, kernel_width // 2
    padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    edge_image = np.zeros_like(image, dtype=np.float32)
    for i in range(img_height):
        for j in range(img_width):
            region = padded_image[i:i + kernel_height, j:j + kernel_width]
            edge_value = np.sum(region * diagonal_left_kernel)
            edge_image[i, j] = edge_value
    edge_image = np.abs(edge_image)  
    edge_image = (edge_image / edge_image.max()) * 255
    diagonal_left_edge_image = edge_image.astype(np.uint8) 
    cv2.imwrite(output_path, diagonal_left_edge_image)
def diagonal_right_edge_detection(image_path, output_path):
    image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    diagonal_right_kernel = np.array([
        [ 2, 1,  0],
        [1,  0, -1],
        [ 0, -1,  -2]
    ], dtype=np.float32)
    img_height, img_width = image.shape
    kernel_height, kernel_width = diagonal_right_kernel.shape
    pad_h, pad_w = kernel_height // 2, kernel_width // 2
    padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    edge_image = np.zeros_like(image, dtype=np.float32)
    for i in range(img_height):
        for j in range(img_width):
            region = padded_image[i:i + kernel_height, j:j + kernel_width]
            edge_value = np.sum(region * diagonal_right_kernel)
            edge_image[i, j] = edge_value
    edge_image = np.abs(edge_image)  
    edge_image = (edge_image / edge_image.max()) * 255
    diagonal_right_edge_image = edge_image.astype(np.uint8) 
    cv2.imwrite(output_path, diagonal_right_edge_image)
def point_sharpening(image_path, output_path):
    image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    point_sharpening_kernel = np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0]
    ], dtype=np.float32)
    img_height, img_width = image.shape
    kernel_height, kernel_width = point_sharpening_kernel.shape
    pad_h, pad_w = kernel_height // 2, kernel_width // 2
    padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    sharpened_image = np.zeros_like(image, dtype=np.float32)
    for i in range(img_height):
        for j in range(img_width):
            region = padded_image[i:i + kernel_height, j:j + kernel_width]
            edge_value = np.sum(region * point_sharpening_kernel)
            sharpened_image[i, j] = edge_value
    sharpened_image = np.clip(sharpened_image, 0, 255)
    point_sharpening_image = sharpened_image.astype(np.uint8) 
    cv2.imwrite(output_path, point_sharpening_image)
def vertical_sharpening(image_path, output_path):
    image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    vertical_sharpening_kernel = np.array([
        [ 0, 1,  0],
        [0,  1, 0],
        [ 0, -1,  0]
    ], dtype=np.float32)
    img_height, img_width = image.shape
    kernel_height, kernel_width = vertical_sharpening_kernel.shape
    pad_h, pad_w = kernel_height // 2, kernel_width // 2
    padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    sharpened_image = np.zeros_like(image, dtype=np.float32)
    for i in range(img_height):
        for j in range(img_width):
            region = padded_image[i:i + kernel_height, j:j + kernel_width]
            edge_value = np.sum(region * vertical_sharpening_kernel)
            sharpened_image[i, j] = edge_value
    sharpened_image = np.clip(sharpened_image, 0, 255)
    vertical_sharpening_image = sharpened_image.astype(np.uint8) 
    cv2.imwrite(output_path, vertical_sharpening_image)
def horizontl_sharpening(image_path, output_path):
    image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    horizontal_sharpening_kernel = np.array([
        [ 0, 0,  0],
        [1,  1, -1],
        [ 0, 0,  0]
    ], dtype=np.float32)
    img_height, img_width = image.shape
    kernel_height, kernel_width = horizontal_sharpening_kernel.shape
    pad_h, pad_w = kernel_height // 2, kernel_width // 2
    padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    sharpened_image = np.zeros_like(image, dtype=np.float32)
    for i in range(img_height):
        for j in range(img_width):
            region = padded_image[i:i + kernel_height, j:j + kernel_width]
            edge_value = np.sum(region * horizontal_sharpening_kernel)
            sharpened_image[i, j] = edge_value
    sharpened_image = np.clip(sharpened_image, 0, 255)
    horizontal_sharpening_image = sharpened_image.astype(np.uint8) 
    cv2.imwrite(output_path, horizontal_sharpening_image)
def diagonal_left_sharpening(image_path, output_path):
    image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    diagonal_left_sharpening_kernel = np.array([
        [ 1, 0,  0],
        [0,  1, 0],
        [ 0, 0,  -1]
    ], dtype=np.float32)
    img_height, img_width = image.shape
    kernel_height, kernel_width = diagonal_left_sharpening_kernel.shape
    pad_h, pad_w = kernel_height // 2, kernel_width // 2
    padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    sharpened_image = np.zeros_like(image, dtype=np.float32)
    for i in range(img_height):
        for j in range(img_width):
            region = padded_image[i:i + kernel_height, j:j + kernel_width]
            edge_value = np.sum(region * diagonal_left_sharpening_kernel)
            sharpened_image[i, j] = edge_value
    sharpened_image = np.clip(sharpened_image, 0, 255)
    diagonal_left_sharpening_image = sharpened_image.astype(np.uint8) 
    cv2.imwrite(output_path, diagonal_left_sharpening_image)
def diagonal_right_sharpening(image_path, output_path):
    image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    diagonal_right_sharpening_kernel = np.array([
        [ 0, 0,  1],
        [0,  1, 0],
        [ -1, 0,  0]
    ], dtype=np.float32)
    img_height, img_width = image.shape
    kernel_height, kernel_width = diagonal_right_sharpening_kernel.shape
    pad_h, pad_w = kernel_height // 2, kernel_width // 2
    padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    sharpened_image = np.zeros_like(image, dtype=np.float32)
    for i in range(img_height):
        for j in range(img_width):
            region = padded_image[i:i + kernel_height, j:j + kernel_width]
            edge_value = np.sum(region * diagonal_right_sharpening_kernel)
            sharpened_image[i, j] = edge_value
    sharpened_image = np.clip(sharpened_image, 0, 255)
    diagonal_right_sharpening_image = sharpened_image.astype(np.uint8) 
    cv2.imwrite(output_path, diagonal_right_sharpening_image)
def fft_image(input_path, output_path):
    image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    fft = np.fft.fft2(image)
    fft_shifted = np.fft.fftshift(fft)

    magnitude_spectrum = np.log1p(np.abs(fft_shifted))

    magnitude_spectrum = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX)
    magnitude_spectrum = magnitude_spectrum.astype(np.uint8)

    cv2.imwrite(output_path, magnitude_spectrum)

    return fft_shifted
def ifft_image(fft_data, output_path):
    fft_unshifted = np.fft.ifftshift(fft_data)

    ifft = np.fft.ifft2(fft_unshifted)

    reconstructed_image = np.abs(ifft)

    reconstructed_image = cv2.normalize(reconstructed_image, None, 0, 255, cv2.NORM_MINMAX)
    reconstructed_image = reconstructed_image.astype(np.uint8)

    cv2.imwrite(output_path, reconstructed_image)
def create_frequency_grid(shape):
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    y, x = np.ogrid[:rows, :cols]
    freq_grid = np.sqrt((x - ccol)**2 + (y - crow)**2)
    return freq_grid
def ideal_filter(image_path, output_path, cutoff, filter_type="low"):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    fft = np.fft.fft2(image)
    fft_shifted = np.fft.fftshift(fft)

    freq_grid = create_frequency_grid(image.shape)

    if filter_type == "low":
        mask = freq_grid <= cutoff
    elif filter_type == "high":
        mask = freq_grid > cutoff
    else:
        raise ValueError("Invalid filter_type. Use 'low' or 'high'.")

    filtered_fft = fft_shifted * mask

    fft_unshifted = np.fft.ifftshift(filtered_fft)
    ifft = np.fft.ifft2(fft_unshifted)
    filtered_image = np.abs(ifft)
    filtered_image = cv2.normalize(filtered_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    cv2.imwrite(output_path, filtered_image)
def gaussian_filter(image_path, output_path, cutoff, filter_type="low"):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    fft = np.fft.fft2(image)
    fft_shifted = np.fft.fftshift(fft)

    freq_grid = create_frequency_grid(image.shape)

    gaussian_low = np.exp(-(freq_grid**2) / (2 * (cutoff**2)))

    if filter_type == "low":
        mask = gaussian_low
    elif filter_type == "high":
        mask = 1 - gaussian_low
    else:
        raise ValueError("Invalid filter_type. Use 'low' or 'high'.")

    filtered_fft = fft_shifted * mask

    fft_unshifted = np.fft.ifftshift(filtered_fft)
    ifft = np.fft.ifft2(fft_unshifted)
    filtered_image = np.abs(ifft)
    filtered_image = cv2.normalize(filtered_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    cv2.imwrite(output_path, filtered_image)
def butterworth_filter(image_path, output_path, cutoff, order, filter_type="low"):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    fft = np.fft.fft2(image)
    fft_shifted = np.fft.fftshift(fft)

    freq_grid = create_frequency_grid(image.shape)

    butter_low = 1 / (1 + (freq_grid / cutoff)**(2 * order))

    if filter_type == "low":
        mask = butter_low
    elif filter_type == "high":
        mask = 1 - butter_low
    else:
        raise ValueError("Invalid filter_type. Use 'low' or 'high'.")

    filtered_fft = fft_shifted * mask

    fft_unshifted = np.fft.ifftshift(filtered_fft)
    ifft = np.fft.ifft2(fft_unshifted)
    filtered_image = np.abs(ifft)
    filtered_image = cv2.normalize(filtered_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    cv2.imwrite(output_path, filtered_image)


