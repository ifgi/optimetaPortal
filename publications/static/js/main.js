const dataCopyright = " | Publication metadata license: <a href='https://creativecommons.org/publicdomain/zero/1.0/'>CC-0</a>";
const publications_url = '/api/publications/';

async function initMap() {
    var map = L.map("map");

    var osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data: &copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors' + dataCopyright,
        maxZoom: 18
    }).addTo(map);

    //var esriWorldImageryLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    //    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community' + dataCopyright,
    //    maxZoom: 18
    //}).addTo(map);

    var baseLayers = {
        "OpenStreetMap": osmLayer,
        //"Esri World Imagery": esriWorldImageryLayer
    };

    publicationsGroup = new L.FeatureGroup();
    map.addLayer(publicationsGroup);

    var overlayMaps = {
        "Publications": publicationsGroup
    };
    
    L.control.scale({ position: 'bottomright' }).addTo(map);
    L.control.layers(baseLayers, overlayMaps).addTo(map);

    var publications = await load_publications();
    var publicationsLayer = L.geoJSON(publications, {
        onEachFeature: publicationPopup
    })
    publicationsLayer.eachLayer(
        function (l) {
            publicationsGroup.addLayer(l);
        });

    map.fitBounds(publicationsGroup.getBounds());
}

function publicationPopup(feature, layer) {
    var popupContent = '<h3>'+ feature.properties['title']+'</h3>' +
        '<l>'+ feature.properties['abstract']+ '</l>'+'<br>'+
        '<a href="http://www.google.com">Visit Article</a>' ;

    if (feature.properties && feature.properties.popupContent) {
        popupContent += feature.properties.popupContent;
    }

    layer.bindPopup(popupContent);
}

async function load_publications() {
    response = await fetch(publications_url);
    geojson = await response.json();
    return geojson;
}

// render publications after page is loaded
$(function () {
    initMap();
});

// email sent alert
$(document).ready(function(){
    $( 'button').click(function() {
        $('.alert').show()
    })
});

