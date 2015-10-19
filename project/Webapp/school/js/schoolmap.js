var town_source = new ol.source.Vector({
  format: new ol.format.GeoJSON(),
  url: function(extent, resolution, projection) {
    return 'http://192.168.1.102:8080/geoserver/wfs?service=WFS&' +
        'version=1.1.0&request=GetFeature&typename=school:town_view&' +
        'outputFormat=application/json&srsname=EPSG:4326&';
  },
  strategy: ol.loadingstrategy.tile(ol.tilegrid.createXYZ({
    maxZoom: 19
  }))
});

var school_source = new ol.source.Vector({
  format: new ol.format.GeoJSON(),
  url: function(extent, resolution, projection) {
    return 'http://192.168.1.102:8080/geoserver/wfs?service=WFS&' +
        'version=1.1.0&request=GetFeature&typename=school:school&' +
        'outputFormat=application/json&srsname=EPSG:4326&';
  },
  strategy: ol.loadingstrategy.tile(ol.tilegrid.createXYZ({
    maxZoom: 19
  }))
});

var ptStyle = new ol.style.Style({
    image: new ol.style.Circle({
        radius: 2,
        fill: new ol.style.Fill({
            color: 'rgba(20,150,200,0.3)'
        }),
        stroke: new ol.style.Stroke({
            color: 'rgba(20,130,150,0.8)',
            width: 1
        })
    })
});

var polyStyle = new ol.style.Style({
  fill: new ol.style.Fill({
    color: '#f1f4c7'
  }),
  stroke: new ol.style.Stroke({
    color: '#afb38a',
    width: 0.26
  }),
  text: new ol.style.Text({
    font: '12px Calibri,sans-serif',
    fill: new ol.style.Fill({
      color: '#000'
    }),
    stroke: new ol.style.Stroke({
      color: '#fff',
      width: 3
    })
  })
});

var styles = [polyStyle];

var schoolLayers = new ol.layer.Group({
    title: 'School',
    layers: [
        new ol.layer.Vector({
            title: "Town",
            source: town_source,
            style: function(feature, resolution) {
                polyStyle.getText().setText(resolution < 200 ? feature.get('town_name') : '');
                return styles;
            }
        }),
        new ol.layer.Vector({
            title: "School",
            source: school_source,
            style: ptStyle
        })
    ]
});

var baseMaps = new ol.layer.Group({
    title: 'Base maps',
    layers: [
        new ol.layer.Tile({
            title: 'Water color',
            type: 'base',
            visible: false,
            source: new ol.source.Stamen({
                layer: 'watercolor'
            })
        }),
        new ol.layer.Tile({
            title: 'OSM',
            type: 'base',
            visible: true,
            source: new ol.source.OSM()
        }),
        new ol.layer.Tile({
            title: 'Satellite',
            type: 'base',
            visible: false,
            source: new ol.source.MapQuest({layer: 'sat'})
        })
    ]
});

var map = new ol.Map({
  controls: ol.control.defaults().extend([
    new ol.control.FullScreen()
  ]),
  layers: [baseMaps, schoolLayers],
  target: document.getElementById('map'),
  view: new ol.View({
    center: ol.proj.transform([120.52, 22.95], 'EPSG:4326', 'EPSG:3857'),
    maxZoom: 19,
    zoom: 9.5
  })
});

var layerSwitcher = new ol.control.LayerSwitcher({
    tipLabel: 'Layer Switcher'
});
map.addControl(layerSwitcher);