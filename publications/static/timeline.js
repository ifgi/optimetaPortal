
async function getarticle() {
    const publications_url = 'http://localhost:8000/api/publications/'
    try {
        let res = await fetch(publications_url);
        return await res.json();
    } catch (error) {
        console.log(error);
    }
}

async function renderarticle() {
    let data = await getarticle();
    console.log('Type:',data.features[0].properties['publicationDate'])
    const f = data.features.length
    for (var index = 0; index < f ; ++index){
        document.getElementById("articles").innerHTML += '<li>' +'<a href="#">' +  data.features[index].properties['title'] + "-" + data.features[index].properties['publicationDate'] +'</a>'+ '</li>';
    }
}

renderarticle();


