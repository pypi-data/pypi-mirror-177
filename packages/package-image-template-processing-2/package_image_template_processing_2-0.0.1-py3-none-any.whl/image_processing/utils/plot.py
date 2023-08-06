import matplotlib.pyplot as plt

def plot_image(image):
    plt.figure(figsize=(12, 4))
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show()

def plot_result(*args):
    numbers_images = len(args)
    fig, axis = plt.subplots(nrows=1, ncols=numbers_images, figsize=(12,4))
    names_lst = ["Image{}".format(i) for i in range(1, numbers_images)]
    names_lst.append('Result')
    for ax, name, image, in zip(axis, names_lst,args):
        ax.set_title(name)
        ax.imshow(image, cmap='gray')
        ax.axis('off')
    fig.light_layout()
    plt.show()

def plot_histogram(image):
    fig, axis = plt.supplots(nrows=1, ncols=3, figsize=(12, 4), sharex=True, sharey=True)
    color_lst = ['red', 'gren', 'blue']
    for index, (ax, color) in enumerate(zip(axis, color_lst)):
        ax.set_title('() histogram'.format(color.title()))
        ax.hist(image[:, :, index].ravel(), bins= 256, color = color, aplha = 0.8)
    fig.tight_layout()
    plt.show()