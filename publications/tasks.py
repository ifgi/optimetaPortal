from django_q.models import Schedule
from publications.models import Publication
from bs4 import BeautifulSoup
import json
import xml.dom.minidom
from django.contrib.gis.geos import GEOSGeometry 
import requests


def get_geom(url):
    req= requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    geom = parse_html(soup)
    geom_object = None
    if geom : 
        geom_data = geom["features"][0]["geometry"]
        # preparing geometry data in accordance to geosAPI fields
        type_geom= {'type': 'GeometryCollection'}
        geom_content = {"geometries" : [geom_data]}
        type_geom.update(geom_content)
        geom_data_string= json.dumps(type_geom)        
        try :
            geom_object = GEOSGeometry(geom_data_string) #GeometryCollection object
        except :
            print("Invalid Geometry") 
    
    return geom_object
    
def parse_html(content):
    json_object = {}
    for tag in content.find_all("meta"):
        if tag.get("name", None) == "DC.SpatialCoverage":
            data = tag.get("content", None)
            try:
                json_object = json.loads(data)                
            except ValueError as e:
                print("Not a valid GeoJSON")
    return json_object
    

def get_timeperiod(url):
    req= requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    return extract_timeperiod_from_html(soup)

def extract_timeperiod_from_html(content):
    tp_start = []
    tp_end = []
    for tag in content.find_all("meta"):
        if tag.get("name", None) == "DC.temporal":
            data = tag.get("content", None)
            period =  data.split("/")
            period1 = period[0]
            period2 = period[1]
            tp_start.append(period1)
            tp_end.append(period2)
    
    return tp_start,tp_end
    

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
            geom_object = get_geom(link_value)          
            #get Timeperiod from html
            period = get_timeperiod(link_value)
            period_start = period[0]
            period_end = period[1]
        else:
            link_value = None
            geom_object = None
            period_start = []
            period_end = []
                
        title = collection.getElementsByTagName("dc:title")
        if title:
            title_value = title[0].firstChild.nodeValue
        else :
            title_value = None
        abstract = collection.getElementsByTagName("dc:description") 
        if abstract:
            abstract_text = abstract[0].firstChild.nodeValue
        else:
            abstract_text = None            
        journal = collection.getElementsByTagName("dc:publisher")
        if journal:
            journal_value = journal[0].firstChild.nodeValue
        else: 
            journal_value = None
        date = collection.getElementsByTagName("dc:date")
        if date:
            date_value = date[0].firstChild.nodeValue
        else:
            date_value = None               
        publication = Publication(title = title_value,abstract = abstract_text,publicationDate = date_value, url = link_value , journal = journal_value, geometry = geom_object, timeperiod_startdate = period_start,timeperiod_enddate = period_end)
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

