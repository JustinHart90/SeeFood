from bs4 import BeautifulSoup

import requests, json
import os
import sys
import urllib.request, json
import pickle
import pymongo


def request():
    # write_data = []
    # for i in range(0,10):
    #     api = str(os.environ.get("FOOD_API"))
    #     page = '&page=' + str(i)
    #     with urllib.request.urlopen('http://food2fork.com/api/search?key='+str(api)+str(page)) as url:
    #         data = url.read()
    #         fdata = json.loads(data)
    #         recipes = fdata['recipes']
    #         for i,x in enumerate(recipes):
    #             write_data.append([recipes[i]['title'],recipes[i]['image_url']] )
    #             print(write_data)
    #dict_keys(['uri', 'label', 'image', 'source', 'url', 'shareAs', 'yield', 'dietLabels', 'healthLabels',
    #'cautions', 'ingredientLines', 'ingredients', 'calories', 'totalWeight', 'totalNutrients', 'totalDaily', 'digest'])
    app = str(os.environ.get("EDAM_APP"))
    api = str(os.environ.get("EDAM_KEY"))
    #connect to mongo
    uri = str(os.environ.get("MONGODB_URI"))
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    micro = db['micro']
    nameList = ['burrito', 'pizza', 'enchilada', 'salmon', 'fish', 'bacon', 'hotdog', 'beef', 'chicken', 'steak']
    write_out = []

    for name in nameList:
        for i in range(1,2):
            start = 1 + (100 * (i-1) )
            stop = 100 + (100 * (i-1) )
            url = 'https://api.edamam.com/search?q='+name+'&app_id=' + app + '&app_key=' + api + '&from='+ str(start) +'&to='+str(stop)
                # payload = {'app_id': str(os.environ.get("EDAM_APP")), 'app_key': str(os.environ.get("EDAM_KEY"))}
            print(url)
            with urllib.request.urlopen(url) as url:
                    data = url.read()
                    fdata = json.loads(data)
                    print(len(fdata['hits']))
                    if len(fdata['hits']) > 0:
                        for i,y in enumerate(fdata['hits']):
                            micro.insert_one({'cat': name, 'key': i, 'label' : fdata['hits'][i]['recipe']['label'],'image_url' : fdata['hits'][i]['recipe']['image'], 'calories' : fdata['hits'][i]['recipe']['calories'], 'totalNutrients' : fdata['hits'][i]['recipe']['totalNutrients']})

        #                     write_out.append({'key': i, 'label' : fdata['hits'][i]['recipe']['label'],'image_url' : fdata['hits'][i]['recipe']['image'], 'calories' : fdata['hits'][i]['recipe']['calories'], 'totalNutrients' : fdata['hits'][i]['recipe']['totalNutrients']})
        # pickle.dump( write_out, open( '../data/'+name+ ".pickle", "wb" ) )



if __name__ == '__main__':
    request()
