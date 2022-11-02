const copy = "© <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors";
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const osm = L.tileLayer(url, { attribution: copy });
const map = L.map("map", { layers: [osm] });
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

async function load_publications() {
    const publications_url = 'http://localhost:8000/api/publications/'
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
