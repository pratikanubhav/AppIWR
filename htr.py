from __future__ import division
from __future__ import print_function


from DataLoader import DataLoader, Batch
from Model import Model, DecoderType
from SamplePreprocessor import preprocess

import shutil
import os
import argparse
import editdistance
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import cv2

from ocr import page, words

 

def textRecog(infilename):
    image = cv2.cvtColor(cv2.imread(infilename), cv2.COLOR_BGR2RGB)
    crop = page.detection(image)
    boxes = words.detection(crop)
    lines = words.sort_words(boxes)
    crop = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
    imLines = []
    for line in lines:
        imLine = []
        for (x1, y1, x2, y2) in line:
            imLine.append(crop[y1:y2, x1:x2])
        imLines.append(imLine)

    #decoderType = DecoderType.WordBeamSearch
    #decoderType = DecoderType.BeamSearch
    decoderType = DecoderType.BestPath

    model = Model(open('./model/charList.txt').read(), decoderType, mustRestore=True)
    #file1 = open("myfile.txt", "w")
    recognizedText = ""

    for line in imLines:
        imgs = []
        for word in line:
            imgs.append(preprocess(word, Model.imgSize))
        batch = Batch(None, imgs)
        (recognized, probability) = model.inferBatch(batch, True)

        l = ""
        for pw in recognized:
            l += pw
            l += ' '
        recognizedText += l
    return recognizedText

 



