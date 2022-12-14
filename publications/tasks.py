from django_q.models import Schedule
from publications.models import Publication
import requests
from bs4 import BeautifulSoup
import json
import xml.dom.minidom
from django.contrib.gis.geos import GEOSGeometry 


def get_geom(url):
    req= requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    return parse_html(soup)
    
def parse_html(content):    
    for tag in content.find_all("meta"):
        if tag.get("name", None) == "DC.SpatialCoverage":
            data = tag.get("content", None)
            try:
                json_object = json.loads(data)
                return(json_object)
            except ValueError as e:
                print("Not a valid GeoJSON")
        else : 
            pass # return None     

def extract_data_from_article(identifier_value):
    pass
    

def parse_xml(content):
    
    DOMTree = xml.dom.minidom.parseString(content)
    collection = DOMTree.documentElement # pass DOMTree as argument
    articles = collection.getElementsByTagName("dc:identifier")                                            
    articles_count_in_journal = len(articles)  # number of articles in journal
    for i in range(articles_count_in_journal):
        identifier = collection.getElementsByTagName("dc:identifier")
        identifier_value = identifier[i].firstChild.nodeValue
        if identifier_value.startswith('http'):
            link_value = identifier_value               
            #get geometry from html
            geom = get_geom(link_value)
            geom_data = geom["features"][0]["geometry"]
            geom_data_string = json.dumps(geom_data)
            # preparing geometry data in accordance to geosAPI fields
            type_geom= {'type': 'GeometryCollection'}
            geom_content = {"geometries" : [geom_data_string]}
            type_geom.update(geom_content)
            geom_data = json.dumps(type_geom)
            # geometry field accept json object as string
            try :
                geom_object = GEOSGeometry(geom_data) #GeometryCollection object
            except :
                print("Invalid Geometry")            
        else:
            link_value = None
            geom_object = None

        title = collection.getElementsByTagName("dc:title")
        title_value = title[0].firstChild.nodeValue
        abstract = collection.getElementsByTagName("dc:description") 
        abstract_text = abstract[0].firstChild.nodeValue
        journal = collection.getElementsByTagName("dc:publisher")
        journal_value = journal[0].firstChild.nodeValue
        date = collection.getElementsByTagName("dc:date")
        date_value = date[0].firstChild.nodeValue                   
        publication = Publication(title = title_value,abstract = abstract_text,publicationDate = date_value, url = link_value , geometry = geom_object,journal = journal_value)
        publication.save()
        

def harvest_data(url):
    try:
        response = requests.get(url)
        parse_xml(response.content)        
    except requests.exceptions.RequestException as e:  
        print ("The requested URL is invalid or has bad connection.Please change the URL")
   


# shell
Schedule.objects.create(
    func= 'publications.tasks.harvest_demo',
    schedule_type=Schedule.MONTHLY
)

