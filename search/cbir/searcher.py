import numpy as np
from django.core.files.storage import FileSystemStorage

from search.cbir.colordescriptor import ColorDescriptor
import cv2

from search.models import Product


class Searcher:
    def __init__(self, query_file, index_file, category=''):
        self.results = {}
        fs = FileSystemStorage()
        fs.save(query_file.name, query_file)
        self.image = cv2.imread('/home/mrt/Work/django/noname/' + query_file.name)
        self.features = ColorDescriptor((8, 12, 3)).describe(self.image)
        self.index_file = index_file
        self.category = category

    def search(self, limit=10):
        for row in self.index_file:
            self.set_result(row)
        self.results = sorted(self.results.items(), key=lambda i: i[1])
        return self.results[:limit]

    def set_result(self, row):
        features = [float(x) for x in row[1:]]
        vf = np.vectorize(lambda a, b: ((a - b) ** 2) / (a + b + 1e-10))
        d = 0.5 * np.sum(vf(features, self.features))
        if d < 15:
            self.results[row[0]] = d

    def set_result2(self, key, row):
        features = [float(x) for x in row]
        vf = np.vectorize(lambda a, b: ((a - b) ** 2) / (a + b + 1e-10))
        d = 0.5 * np.sum(vf(features, self.features))
        if d < 15:
            self.results[key] = d

    def search2(self, limit=10):
        products = Product.objects.filter(category=self.category)

        for product in products:
            self.set_result2(product.product_src_id, self.index_file[product.product_src_id])
        self.results = sorted(self.results.items(), key=lambda i: i[1])
        return self.results[:limit]





