# Met Data Pipeline
# TODO: Write function to reize images
# TODO: Remove unnecessary columns
# TODO: Trim borders or focus on central 3/5ths
# TODO: make list of images already downloaded/processed



import numpy as np
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import time

classifications = ['Drawings', 'Paintings', 'Prints', 'Portraits', 'Miscellaneous-Paintings & Portraits', 'Painted Canvases', 'Pastels & Oil Sketches on Paper', 'Paper-Drawings', 'Paintings-Frescoes', 'Drawings|Paintings', 'Paintings|(not assigned)', 'Paintings-Panels', 'Paintings|Drawings', 'Prints|Drawings', 'Miscellaneous|Paintings', 'Paintings|Prints' ]

class Met():
    def load_raw_csv(self):
        try:
            self.raw = pd.read_csv('../openaccess/MetObjects.csv')
            print("{} pieces of art loaded.".format(self.raw.shape[0]))
        except:
            print('Error on load_raw_csv')

    def filter_paintings(self):
        self.paintings = self.raw[self.raw.Classification == 'Paintings']
        print("{} paintings loaded.".format(self.paintings.shape[0]))

    def filter_is_public_domain(self):
        self.paintings = self.paintings[self.paintings['Is Public Domain'] == True]
        print("{} paintings are public domain.".format(self.paintings.shape[0]))

    def _get_jpg_from_web(self,painting):
        s_link = painting['Link Resource']
        filename = "images/Met/{}.jpg".format(painting['Object ID'])
        with urllib.request.urlopen(s_link) as response:
            webpage = response.read()
        soup = BeautifulSoup(webpage, 'html.parser')
        image_link = soup.find('meta', {'property':'og:image'})['content']
        try:
            urllib.request.urlretrieve(image_link, filename)
        except:
            print('Error on saving, sleeping')


    def get_all_jpgs(self):
        count = 0
        for index, painting in self.paintings.iterrows():
            print('Count: {}, Index: {}'.format(count,index))
            self._get_jpg_from_web(painting)
            time.sleep(np.random.randint(0,5))
            count +=1

if __name__ == '__main__':
    met = Met()
    met.load_raw_csv()
    met.filter_paintings()
    met.filter_is_public_domain()
    met.get_all_jpgs()
