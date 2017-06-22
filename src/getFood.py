from bs4 import BeautifulSoup

import requests, json
import os
import sys
import urllib.request, json
import pickle
import pymongo


def request():
    # The API keys
    #dict_keys(['uri', 'label', 'image', 'source', 'url', 'shareAs', 'yield', 'dietLabels', 'healthLabels',
    #'cautions', 'ingredientLines', 'ingredients', 'calories', 'totalWeight', 'totalNutrients', 'totalDaily', 'digest'])
    app = str(os.environ.get("EDAM_APP"))
    api = str(os.environ.get("EDAM_KEY"))
    #connect to mongo
    uri = str(os.environ.get("MONGODB_URI"))#connect to your Mlab
    client = pymongo.MongoClient(uri)# dont worry bout it
    db = client.get_default_database()# dont worry bout it
    micro = db['micro']# name the db of collections
    nameList = ['tacos']
    write_out = []
    #run the script for for the amount of keywords you want
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
