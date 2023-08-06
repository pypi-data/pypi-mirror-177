from high_pass_filters.image import get_image
import numpy as np

s3x3 = np.asarray([[1, 0, -1],
                   [2, 0, -2],
                   [1, 0, -1]])

s5x5 = np.asarray([[2, 2, 4, 2, 2],
                   [1, 1, 2, 1, 1],
                   [0, 0, 0, 0, 0],
                   [-1, -1, -2, -1, -1],
                   [-2, -2, -4, -2, -2]])


def convolution2d(image, kernel, bias):
    global new_image
    m, n = kernel.shape
    if m == n:
        y, x = image.shape
        y = y - m + 1
        x = x - m + 1
        new_image = np.zeros((y,x))
        for i in range(y):
            for j in range(x):
                new_image[i][j] = np.sum(image[i:i+m, j:j+m]*kernel) + bias

    return new_image


def operador_direcional(img, gx):
    gy = gx.T
    Gx = convolution2d(img, gx, 1)
    Gy = convolution2d(img, gy, 1)

    return np.sqrt(Gx ** 2 + Gy ** 2)


def sobel(img, mascara=s3x3):
    """
    O filtro Sobel utiliza duas máscaras deslocadas em 90° para encontrar os gradientes verticais
    e horizontais das bordas semelhante ao operador de Prewitt, porém com mais peso nos pontos
    próximos ao pixel central. Por esse motivo, a máscara de Sobel obtém as bordas mais destacadas
    em relação ao operador de Prewitt sendo muito menos sensível ao ruído.
    :param mascara:
    :param img:
    :return:
    """
    return operador_direcional(img[:, :, 0], mascara)
