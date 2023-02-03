const container = document.getElementById("timeline");
    
// Create a DataSet (allows two way data-binding)
const articles = new vis.DataSet([
    { id: 1, content: "article 1", start: "2007-03-05", end: "2015-10-10" },
    { id: 2, content: "article 2", start: "2005-08-23", end: "2013-06-01" },
    { id: 3, content: "article 3", start: "2015-08-20", end: "2018-04-26"},
    { id: 4, content: "article 4", start: "2004-01-11", end: "2005-02-25" },
    { id: 5, content: "article 5", start: "2011-03-12", end: "2014-10-11"},
    { id: 6, content: "article 6", start: "2002-02-25", end : "2013-02-25" , title : '<b>titleofarticle</b><br><p>Journal</p>'},
    { id: 7, content: "article 7", start: "2003-08-04", end: "2012-07-08" },
    { id: 8, content: "article 8", start: "2011-03-18", end: "2011-10-28" },
    { id: 9, content: "article 9", start: "2011-06-04", end: "2014-09-29" },
    { id: 10, content: "article 10", start: "2006-08-27", end: "2013-02-24" },
    { id: 11, content: "article 11", start: "2002-01-28", end: "2004-10-19" },
    { id: 12, content: "article 12", start: "2007-11-21", end: "2012-09-25" },
    { id: 13, content: "article 13", start: "2005-01-20", end: "2011-04-20" },
    { id: 14, content: "article 14", start: "2009-03-24", end: "2014-11-23" },
    { id: 15, content: "article 15", start: "2002-10-16", end: "2008-02-20" },
    { id: 16, content: "article 16", start: "2001-08-07", end: "2005-07-06" },
    { id: 17, content: "article 17", start: "2006-12-24", end: "2015-11-04" },
    { id: 18, content: "article 18", start: "2009-07-05", end: "2015-08-30" },
    { id: 19, content: "article 19", start: "2014-06-02", end: "2015-05-20" },
    { id: 20, content: "article 20", start: "2002-09-12", end: "2010-08-08" },
    { id: 21, content: "article 21", start: "2008-03-04", end: "2013-05-04" },
    { id: 22, content: "article 22", start: "2010-02-21", end: "2015-07-31" },
    { id: 23, content: "article 23", start: "2004-10-30", end: "2006-04-07" },
    { id: 24, content: "article 24", start: "2000-06-15", end: "2003-08-13" },
    { id: 25, content: "article 25", start: "2011-03-19", end: "2014-10-29" },
]);

// Configuration for the Timeline
const options = {
    stack: true,
    verticalScroll: true,
    zoomKey: 'ctrlKey',
    maxHeight: 600,
    timeAxis: {scale: 'year', step: 2},
    start : "2000-01-01",   
};

// Create a Timeline
timeline = new vis.Timeline(container, articles, options);
//timeline.setWindow('2010-05-01', '2019-04-01');







