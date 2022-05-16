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

        r = [None for i in range(5)]
        diff = (high-low)//10
        for i in range(11):
            r.append((low+(i*diff)))
        self.operations.append(randomcrop)
        self.args.append(r)

    def addJitter(self, types):
        r = [None for i in range(2)]
        s = set(["b", "s", "c"])
        for i in types:
            if i not in s:
                raise "Invalid type"
        self.operations.append(colorjitter)
        r.extend(types)
        self.args.append(r)

    def addNoise(self, types):
        r = [None for i in range(2)]
        s = set(["gauss", "sp"])
        for i in types:
            if i not in s:
                raise "Invalid type"
        self.operations.append(noisy)
        r.extend(types)
        self.args.append(r)

    def addFilter(self, types):
        r = [None for i in range(2)]
        s = set(["blur", "gaussian", "median"])
        for i in types:
            if i not in s:
                raise "Invalid type"
        self.operations.append(filters)
        r.extend(types)
        self.args.append(r)

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
    p.addNoise(["gauss", "sp"])
    p.addJitter(["b", "c", "s"])
    p.addFilter(["gaussian", "blur", "median"])
    res = p.processOne(im)
    cv2.imshow("Result", res)
    
    while True : 
        k = cv2.waitKey()
        if k==27 : 
            break
        
        
