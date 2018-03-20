/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

com.sweattrails.PrettyMap = function (gpx, mapid) {
    this.url = gpx;
    this.mapid = mapid;
    if (!this.url || !this.mapid) return;

    this.map = L.map(this.mapid, {
        renderer: L.canvas(),
        preferCanvas: true
    });
    this.osm = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        theme: "light",
        // attribution: 'Map data &#169; &lt;a href="http://www.osm.org"&gt;OpenStreetMap&lt;/a&gt'
        attribution: 'Map data (c) OpenStreetMap contributors'
    }).addTo(this.map);
    this.osm_bike = L.tileLayer('http://{s}.tile.opencyclemap.org/cycle/{z}/{x}/{y}.png', {
        theme: "light",
        attribution: 'Map data (c) OpenStreetMap contributors'
    }).addTo(this.map);
    this.mapbox_dark = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data (c) OpenStreetMap contributors, CC-BY-SA, Imagery (c) Mapbox',
        theme: "dark",
        id: 'mapbox.dark',
        accessToken: 'pk.eyJ1IjoiamFuZGV2IiwiYSI6ImNpenBzbzFzNTAwcmgycnFnd3QycWFpbTgifQ.vIht_WItDuJwLuatY_S5xg'}).addTo(this.map);
    this.mapbox_rbh = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        theme: "light",
        attribution: 'Map data (c) OpenStreetMap contributors, CC-BY-SA, Imagery (c) Mapbox',
        id: 'mapbox.run-bike-hike',
        accessToken: 'pk.eyJ1IjoiamFuZGV2IiwiYSI6ImNpenBzbzFzNTAwcmgycnFnd3QycWFpbTgifQ.vIht_WItDuJwLuatY_S5xg'}).addTo(this.map);

    this.control = L.control.layers({
            "openstreetmap": this.osm,
            "openstreetmap Cycle": this.osm_bike,
            "Mapbox Dark": this.mapbox_dark,
            "Mapbox Run Bike Hike": this.mapbox_rbh
        }
        , null).addTo(this.map);
    this.gpx = null;
    this._elevation = null;
    this._logolayer = new L.layerGroup().addTo(this.map);
    this._iconlayers = {
        elevation: { label: "Elevation Profile", draw: this.elevation },
        logo: { label: "Logo", icon: "runwaterloo.png", size: new L.point(200, 90) },
        water: { label: "Water Station", icon: "water.png" },
        firstaid: { label: "First Aid", icon: "firstaid.png" },
        police: { label: "Police", icon: "police.png" }
    };
    for (var l in this._iconlayers) {
        var layer = this._iconlayers[l];
        layer.group = new L.layerGroup().addTo(this.map);
        this.control.addOverlay(layer.group, layer.label);
        layer._icons = [];
    }
    this.map.on("click", this.click, this)
        // .on("dblclick", this.dblclick, this)
    ;
};

com.sweattrails.PrettyMap.prototype.click = function(e) {
    if (!this._click) {
        this._click = e;
    } else {
        this.dropIcon(this._click, e);
        this._click = null;
    }
};

// com.sweattrails.PrettyMap.prototype.dblclick = function(e) {
//     this.dropIcon(e);
// };

com.sweattrails.PrettyMap.prototype.dropIcon = function(ev1, ev2) {
    var layer = null;
    var inputs = document.getElementById("iconChoices").getElementsByTagName("input");
    for (var ix = 0; ix < inputs.length; ix++ ) {
        var input = inputs.item(ix);
        if (input.checked) {
            layer = this._iconlayers[input.value];
        }
    }
    if (layer) {
        if (layer.draw) {
            layer.draw.bind(this)(layer, ev1, ev2);
        } else {
            var sz;
            if (!ev2 || (ev1.layerPoint.distanceTo(ev2.layerPoint) < Math.sqrt(2048))) {
                sz = (layer.size) ? layer.size : new L.point(32, 32);
            } else {
                sz = ev2.layerPoint.subtract(ev1.layerPoint);
            }
            layer._icons.push(L.marker(ev1.latlng, {
                    icon: new L.icon({iconUrl: layer.icon, iconSize: sz, iconAnchor: [0, 0]}),
                    draggable: true
                }).addTo(layer.group));
        }
    }
};

com.sweattrails.PrettyMap.prototype.displayGPX = function (onloaded) {
    var _this = this;
    var cb = onloaded;
    this.gpx = new L.GPX(this.url, {
        async: true,
        marker_options: {
            startIconUrl: '/image/pin-icon-start.png',
            endIconUrl:   '/image/pin-icon-end.png',
            shadowUrl:    '/image/pin-shadow.png',
        },
        polyline_options: {
            weight: 5,
            color: '#4e95ff'
        }
    }).on('loaded', function(e) {
        var gpx = e.target;
        _this.map.fitBounds(gpx.getBounds());
        _this.control.addOverlay(gpx, gpx.get_name());
        if (cb) {
            cb(_this);
        }
    });
    this.gpx.addTo(this.map);
};

com.sweattrails.PrettyMap.prototype.elevation = function (layer, ev1, ev2) {
    var west = Math.min(ev1.latlng.lng, ev2.latlng.lng);
    var east = Math.max(ev1.latlng.lng, ev2.latlng.lng);
    var south = Math.min(ev1.latlng.lat, ev2.latlng.lat);
    var north = Math.max(ev1.latlng.lat, ev2.latlng.lat);
    var max_elev = this.gpx.get_elevation_max();
    var min_elev = this.gpx.get_elevation_min();
    var diff_elev = max_elev - min_elev;
    var elev = this.gpx.get_elevation_data();
    var y_scale = (north - south) / diff_elev;
    var x_scale = (east - west) / this.gpx.get_distance();

    L.rectangle([ [ south, west ], [ north, east ] ], { color: '#d1784c' }).addTo(layer.group);
    var data = [];
    for (var ix = 0; ix < elev.length; ix++) {
        var point = elev[ix];
        var x = (parseFloat(point[0])*1000)*x_scale;
        var y = (parseFloat(point[1]) - min_elev) * y_scale;
        // console.log("ix: " + ix + " x: " + x, " y: " + y);
        data.push([ south + y, west + x ]);
    }
    L.polyline(data, { color: '#d1784c' }).addTo(layer.group);
};

com.sweattrails.PrettyMap.prototype.renderImage = function(images) {
    var _ = this;
    _.img = document.createElement('img');
    var dimensions = _.map.getSize();
    _.img.width = dimensions.x / 2;
    _.img.height = dimensions.y / 2;
    _.img.src = "throbber.gif";
    document.getElementById(images).appendChild(_.img);
    leafletImage(this.map, function(err, canvas) {
        _.img.src = canvas.toDataURL();
    });
};

com.sweattrails.PrettyMap.prototype.download = function(img, name) {
    var link = document.createElement("a");
    link.download = (name) ? name : "prettymap.png";
    link.href = img.src;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    delete link;
};
