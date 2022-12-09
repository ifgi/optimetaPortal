from django_q.models import Schedule
from publications.models import Publication
import requests
from bs4 import BeautifulSoup
import json
import xml.dom.minidom
from django.contrib.gis.geos import GEOSGeometry

def harvest_demo():
    url1 = 'https://service.tib.eu/optimeta/index.php/optimeta/oai/?verb=ListRecords&metadataPrefix=oai_dc'
    harvest_data(url1)

def get_geom(url):
    #soup = BeautifulSoup(open(url,encoding="utf8"), "html.parser") # forlocal file
    req= requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    return parse_html(soup)
    
def parse_html(content):    
    for tag in content.find_all("meta"):
        if tag.get("name", None) == "DC.SpatialCoverage":
            data = tag.get("content", None)
            json_object = json.loads(data)
            return(json_object)
        else : 
            pass # return None     

def harvest_data(url):
    # url1 = os.path.join(os.getcwd(),'harvesting\\journal_1\\oai_dc.xml') # forlocalfile
    response = requests.get(url)
    DOMTree = xml.dom.minidom.parseString(response.content)
    collection = DOMTree.documentElement
    articles = collection.getElementsByTagName("dc:identifier")                                            
    articles_count_in_journal = len(articles)  # number of articles in journal
    for i in range(articles_count_in_journal):
        identifier = collection.getElementsByTagName("dc:identifier")
        identifier_value = identifier[i].firstChild.nodeValue
        if identifier_value.startswith('https://'):
            link_value = identifier_value               
            #get geometry from html
            #identifier_url = os.path.join(os.getcwd(),'harvesting\\journal_1\\article_01.html')
            geom = get_geom(link_value)
            geom_data = geom["features"][0]["geometry"]
            geom_data_string = json.dumps(geom_data)
            # preparing geometry data in accordance to geosAPI fields
            type_geom= {'type': 'GeometryCollection'}
            geom_content = {"geometries" : [geom_data_string]}
            type_geom.update(geom_content)
            geom_data = json.dumps(type_geom)
            # geometry field accept json object as string
            geom_object = GEOSGeometry(geom_data) #GeometryCollection object
            #bounds=MultiPolygon([Polygon(((-117.869537353516, 33.5993881225586),(-117.869537353516, 33.7736549377441),(-117.678024291992, 33.7736549377441),(-117.678024291992, 33.5993881225586),(-117.869537353516, 33.5993881225586)))])           
            #gc = GeometryCollection(Point(0, 0), MultiPoint(Point(0, 0), Point(1, 1)), bounds)
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


# shell
Schedule.objects.create(
    func= 'publications.tasks.harvest_demo',
    schedule_type=Schedule.MONTHLY
)

