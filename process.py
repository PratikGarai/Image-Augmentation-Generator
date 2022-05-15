from utils import randomcrop, colorjitter, noisy, filters
import cv2
import random


class Pipeline:

    def __init__(self):
        self.operations = []
        self.args = []

    def addCrop(self, low, high):
        low = float(low)
        high = float(high)
        if low <= 0. or low >= 1.:
            raise "Invalid low value"
        if high <= 0. or high >= 1.:
            raise "Invalid high value"
        if low >= high:
            raise "Invalid low high combination"

        r = [None]
        diff = (high-low)//10
        for i in range(11):
            r.append((low+(i*diff)))
        self.operations.append(randomcrop)
        self.args.append(r)

    def addJitter(self, types):
        r = [None]
        s = set(["b", "s", "c"])
        for i in types:
            if i not in s:
                raise "Invalid type"
        self.operations.append(colorjitter)
        self.args.append(types)

    def addNoise(self, types):
        r = [None]
        s = set(["gauss", "sp"])
        for i in types:
            if i not in s:
                raise "Invalid type"
        self.operations.append(noisy)
        self.args.append(types)

    def addFilter(self, types):
        r = [None]
        s = set(["blur", "gaussian", "median"])
        for i in types:
            if i not in s:
                raise "Invalid type"
        self.operations.append(filters)
        self.args.append(types)

    def processOne(self, img):
        res = img.copy()
        for i in range(len(self.operations)):
            arg = random.choice(self.args[i])
            if arg != None:
                res = self.operations[i](res, arg)
        return res


if __name__ == "__main__":
    im = cv2.imread("sample.jpeg")
    im = cv2.resize(im, (600, 600))
    p = Pipeline()
    p.addCrop(0.75, 0.95)
    p.addNoise(["gauss"])
    p.addJitter(["b", "c"])
    p.addFilter(["gaussian", "blur"])
    res = p.processOne(im)
    cv2.imshow("Result", res)
    
    while True : 
        k = cv2.waitKey()
        if k==27 : 
            break
        
        
