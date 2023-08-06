import matplotlib.image as img
import matplotlib.pyplot as plt


def get_image(path):
    return img.imread(path)


def plot_image(image):
    plt.imshow(image, cmap='gray')
    plt.show()