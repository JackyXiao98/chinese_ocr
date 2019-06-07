# -*- coding:utf-8 -*-

import ocr
import time
import numpy as np


def pic2word(pic):
    # image = np.array(Image.open(image_file).convert('RGB'))
    image = np.array(pic)
    t = time.time()
    # result: the text
    # image_framed: the image with segmentation
    result, image_framed = ocr.model(image)
    print("Mission complete, it took {:.3f}s".format(time.time() - t))
    print("\nRecognition Result:\n")
    f1 = open('word.txt', 'w')
    f2 = open('to_english.txt', 'w')
    for key in result:
        # print(result[key][1])
        f2.write(result[key][1])
        f1.write(result[key][1]+'\n')

