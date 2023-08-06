from high_pass_filters.image import get_image
import numpy as np

p3x3 = np.asarray([[-1, 0, 1],
                   [-1, 0, 1],
                   [-1, 0, 1]])

p5x5 = np.asarray([[9, 9, 9, 9, 9],
                   [9, 5, 5, 5, 9],
                   [-7, -3, 0, -3, -7],
                   [-7, -3, -3, -3, -7],
                   [-7, -7, -7, -7, -7]])


def convolution2d(image, kernel, bias):
    global new_image
    m, n = kernel.shape
    if m == n:
        y, x = image.shape
        y = y - m + 1
        x = x - m + 1
        new_image = np.zeros((y, x))
        for i in range(y):
            for j in range(x):
                new_image[i][j] = np.sum(image[i:i + m, j:j + m] * kernel) + bias

    return new_image


def prewit(img, mascara=p3x3, horizontal=True):
    """
    O filtro Prewitt utiliza duas máscaras que são convoluídas com a imagem original
     para calcular as derivadas nas direções vertical e horizontal. esse operador é
     mais simples de ser implementado que o Sobel, mas apresenta mais ruídos.
    :param horizontal:
    :param mascara:
    :param img:
    :return:
    """


    if horizontal:
        img_prewit = convolution2d(img[:, :, 0], mascara, 1)  # máscara 3x3 na horizontal
    else:
        img_prewit = convolution2d(img[:, :, 0], mascara.T, 1)  # máscara 3x3 na vertical

    return img_prewit
