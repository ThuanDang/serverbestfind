import csv
import json
from difflib import SequenceMatcher

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from search.cbir.searcher import Searcher
from search.models import Product, Shop
from search.serializers import ProductSerializer

index_key_values = {}
index_array = []


def read_index(path):
    print('vao day')

    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            index_array.append(row)
            index_key_values[row[0][:len(row[0]) - 4]] = row[1:]


read_index('/home/mrt/Work/django/noname/index.csv')


def import_db(request):
    if request.method == 'POST' and request.FILES['my_file']:
        my_file = request.FILES['my_file'].read().decode('utf-8')
        data = json.loads(my_file)
        for item in data['result']:
            shop = Shop(name=item['shop']['name'], address=item['shop']['address'],
                        phone=item['shop']['phone'], email=item['shop']['email'],
                        longitude=item['shop']['location']['longitude'], latitude=item['shop']['location']['latitude'],
                        shop_src_id=item['shop']['shopId'])
            shop.save()
            product = Product(name=item['name'], price=float(item['price']), image_link=item['image'],
                              category=item['category'], product_link=item['link'],
                              product_src_id=item['productId'], description=item['description'],
                              shop=shop)
            product.save()
        return render(request, 'success.html')
    return render(request, 'import.html')


@api_view(['POST'])
def search(request):
    if request.method == 'POST' and request.FILES['photo']:
        my_file = request.FILES['photo']
        category = request.POST['category']
        print(category)

        if category == '':
            searcher = Searcher(query_file=my_file, index_file=index_array)
            results = searcher.search()
            products = Product.objects.filter(product_src_id__in=[tup[0][:len(tup[0]) - 4] for tup in results])
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            searcher = Searcher(query_file=my_file, index_file=index_key_values, category=category)
            results = searcher.search2()
            products = Product.objects.filter(product_src_id__in=[tup[0] for tup in results])
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_200_OK)


def import_index(request):
    if request.method == 'POST' and request.FILES['my_file']:
        my_file = request.FILES['my_file']
        fs = FileSystemStorage()
        fs.save('index.csv', my_file)
        return render(request, 'success.html')
    return render(request, 'import.html')


@api_view(['POST'])
def suggestion(request):
    if request.method == 'POST':

        category = request.POST['category']
        name = request.POST['name']
        products = Product.objects.filter(category=category)
        distances = [SequenceMatcher(None, name, product.name).ratio() for product in products]
        distances.sort(reverse=True)
        results = products.filter()
        serializer = ProductSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)