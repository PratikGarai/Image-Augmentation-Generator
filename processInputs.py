import os
from process import Pipeline
import cv2

if __name__ == "__main__":

    replicas = 10
    p = Pipeline()
    p.addCrop(0.75, 0.95)
    p.addNoise(["gauss"])
    p.addJitter(["b", "c"])
    p.addFilter(["gaussian", "blur"])
    
    for fname in os.listdir("inputs"):
        name, extension = fname.split(".")
        im = cv2.imread(os.path.join("inputs", fname))
        for i in range(replicas):
            res = p.processOne(im)
            cv2.imwrite(os.path.join("outputs", f"{name}_{i}.{extension}"), res)
