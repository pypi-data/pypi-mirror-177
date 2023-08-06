
from matplotlib import pyplot as plt
import io
import base64

def encode_image(arr,
title: str = '',
format : str = 'jpg',
figsize: tuple = (8, 8),
cmap: str = "gray"):
    fig = plt.figure(figsize=figsize)
    plt.imshow(arr, cmap=cmap)
    plt.suptitle(title, fontsize=16)
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format=format)
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
    return my_base64_jpgData