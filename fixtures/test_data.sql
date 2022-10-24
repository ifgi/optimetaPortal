-- Draw geometry at https://geojson.io/#map=10.92/51.902/7.6702
-- possibly need to convert to GeometryCollection from FeatureCollection if we face that in GeoJSON the wild: https://gis.stackexchange.com/questions/177254/create-a-geosgeometry-from-a-featurecollection-in-geodangoINSERT INTO public.publications_publication VALUES

INSERT INTO public.publications_publication VALUES
  (1, 'The First Article', 'This is the first article. It is good in Münster.', '2010-10-10 10:10:10', ST_GeomFromGeoJSON('
    {
        "type": "GeometryCollection",
        "geometries": [{
            "coordinates": [7.595730774920725,51.96944097112328],
            "type": "Point",
            "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
        }, {
            "type": "Polygon",
            "coordinates": [[
                [7.599984296478425,51.984257653537384],
                [7.5715788777530975,51.97057414651397],
                [7.570122189613329,51.950602187631205],
                [7.580319006590855,51.93825551711683],
                [7.609054957094401,51.93035649564658],
                [7.659674869951374,51.942256350721436],
                [7.6833460522228165,51.968514669138415],
                [7.665137450475669,51.99229098076532],
                [7.626171042736502,51.98982421450293],
                [7.599984296478425,51.984257653537384]
            ]]
        }]
    }'), now(), now(), '10.5555/12345678', NULL),
  (2, 'Paper Two', 'A second article. It is better; from Hanover to Berlin.', '2011-11-11 11:11:11', ST_GeomFromGeoJSON('
    {
        "type": "GeometryCollection",
        "geometries": [{
            "type": "LineString",
            "coordinates": [
                [9.754609563397707,52.36630414438588],
                [9.813062794192035,52.41569645624003],
                [10.141300167111496,52.36904961184797],
                [10.518997966087937,52.330597538337116],
                [10.838242534270051,52.311358956793185],
                [11.058566250338231,52.220550088821824],
                [11.535184901427073,52.15714903642342],
                [12.272594889905236,52.24258143981572],
                [12.618817872299417,52.35532056817789],
                [12.911084026269464,52.2976119913985],
                [13.144896949445211,52.50063147184562],
                [13.396695482095708,52.517051586549286]
            ]
        }]
    }'), now(), now(), NULL, 'http://paper.url/two')
