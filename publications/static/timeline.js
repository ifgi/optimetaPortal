var content = '{"contents":['+
'{ "name": "Article1", "date": "1997-10-19"},'+
'{ "name": "Article2", "date": "2001-05-06"},'+
'{ "name": "Article3", "date": "2021-09-05"}]}'

const obj = JSON.parse(content);

for (var index = 0; index < 3; ++index){
    document.getElementById("articles").innerHTML += '<li>' +  obj.contents[index].name + "-" + obj.contents[index].date + '</li>';
}



