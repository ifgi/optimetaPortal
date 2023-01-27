
async function getarticle() {
    try {
        let response = await fetch(publications_url);
        let body = await response.json();
        return body.results;
    } catch (error) {
        console.log(error);
    }
}

async function renderarticle() {
    let data = await getarticle();
    console.log('Type:', data.features[0].properties['publicationDate'])
    const f = data.features.length
    for (var index = 0; index < f ; ++index){
        document.getElementById("timeline").innerHTML += '<li>' +'<a href="#">' +  data.features[index].properties['title'] + "-" + data.features[index].properties['publicationDate'] +'</a>'+ '</li>';
    }
}

renderarticle();


