
import pandas as pd
import requests
import urllib.request
from scipy.misc import imread, imsave, imresize, fromimage
from PIL import Image
import io

def main():
    d = pd.read_pickle("../data/all_data.pkl")
    print(d)
    # df = pd.DataFrame(d)
    return (d)

def test(link):
    response = urllib.request.urlopen(link)
    data = io.BytesIO(response.read())
    im = Image.open(data)
    imgdata = fromimage(im, flatten=False, mode='RGB')
    
    imgresized = imresize(imgdata, size = (150,150))


    if imgdata.shape == (300, 300, 3):
        pass

if __name__ == '__main__':
    x = main()
    # test("https://s3.amazonaws.com/dis-capstone-seefood/bacon/0.jpg")

    #
    # from PIL import Image
    # import io

    # res = dance.urlopen(link)
    # data = io.BytesIO(res.read())
    # im = Image.open(data)
    # imgdata = fromimage(im, flatten=False, mode='RGB')
    #
    # imgresized = imresize(imgdata, size = (300,300))
