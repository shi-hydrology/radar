import os.path
import numpy as np
import matplotlib.pyplot as plt

source_dir = "/home/antonv/data/lena/"


def to_2d(x, size):
    data = np.reshape(x, (-1, size))
    # data = np.flipud(data)
    # data = np.fliplr(data)
    data = np.rot90(data, 1)
    return data


def show_me(x):
    plt.imshow(data)
    plt.title(file)
    plt.clim(0, 130)
    plt.colorbar()
    plt.show()
    plt.clf()


for file in os.listdir(source_dir):
    ext = file.split(".")[-1]
    if ext == "bin":
        full_name = os.path.join(source_dir, file)
        print(full_name)
        bin_file = open(full_name, "rb")
        # print(os.path.getsize(full_name))
        array = np.fromfile(bin_file, dtype="uint8")
        # print(array.shape)

        if array.shape[0] == 63504:
            data = to_2d(array, 252)

        elif array.shape[0] == 254016:
            data = to_2d(array, 504)

        else:
            print("Unable to reshape, truncating")
            array = array[0:63504]
            # print(array.shape[0])
            data = to_2d(array)

        show_me(data)
