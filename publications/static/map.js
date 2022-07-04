const copy = "© <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors";
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const osm = L.tileLayer(url, { attribution: copy });
const map = L.map("map", { layers: [osm] }).setView([39.74739, -105], 5);
map.fitWorld();


/*popup*/
function onEachFeature(feature, layer) {
    var popupContent = 'shows the title of artcile ' +
        '<a href="http://www.google.com"><h1> Visit Article</h1></a>' ;

    if (feature.properties && feature.properties.popupContent) {
        popupContent += feature.properties.popupContent;
    }

    layer.bindPopup(popupContent);
}

/*geometry*/
var geojsonFeature = [{
    "type": "Feature",
    "properties": {
        "name": "iceland"       
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [-104.05, 48.99],
            [-97.22,  48.98],
            [-96.58,  45.94],
            [-104.03, 45.94],
            [-104.05, 48.99]
        ]]
    }
},{
    "type": "Feature",
    "properties": {
        "name": "ireland"       
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [-109.05, 41.00],
            [-102.06, 40.99],
            [-102.03, 36.99],
            [-109.04, 36.99],
            [-109.05, 41.00]
        ]]
    }
}];


/*add geojson to map*/
L.geoJSON(geojsonFeature, {
    onEachFeature: onEachFeature
}).addTo(map);

async function load_publications() {
    const publications_url = 'http://localhost:8000/publications/api/publications/'
    const response = await fetch(publications_url)
    const geojson = await response.json()
    return geojson
}

async function render_publications() {
    const publications = await load_publications();
    L.geoJSON(publications, {
        onEachFeature: onEachFeature
    })   
    .addTo(map);
}

map.on("moveend", render_publications);
