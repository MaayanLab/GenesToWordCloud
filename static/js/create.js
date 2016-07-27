var view = $('#view');

// Properties
var width = 960;
var height = 600;
var rotation, rotation_proba, shape;
var font, font_scale, font_size;
var text_case, tags = [], freqs = [];

var last_data, fontSize;

function draw() {
	var max_freq = Math.max.apply(Math, tags.map(function(d) { return d[1]; }));
	view.height(height * view.width() / width);
	WordCloud(view[0], {
		clearCanvas: true,
		shuffle: true,
		list: tags.map(function(t) { return [text_case(t[0]), t[1]] }),
		fontFamily: font,
		gridSize: Math.round(16 * $('#view').width() / 1024), // TODO?
		weightFactor: function (size) { return font_scale(size / max_freq); },
		rotateRatio: rotation_proba,
		minRotation: rotation[0],
		maxRotation: rotation[1],
		shape: shape
	});
	// TODO: wordcloudstart
	// TODO: wordclouddrawn
	// TODO: wordcloudstop
}

function scale_lookup(scale) {
	if(scale == 'ordinal') {
		return function (s) {
			return font_size[0] + s * (font_size[1]-font_size[0]);
		};
	}
	else if(scale == 'log') {
		return function (s) {
			var r = font_size[1] / font_size[0];
			return font_size[0] + Math.log(1 + s * (r - 1)) / Math.log(r) * (font_size[1] - font_size[0]);
		};
	}
	else if(scale == 'sqrt') {
		return function (s) {
			return font_size[0] + Math.sqrt(s) * (font_size[1] - font_size[0]);
		};
	}
}

function case_lookup(c) {
	// return the case function for the specified case
	if(c == 'lower')
		return function(t) { return t.toLowerCase(); };
	else if(c == 'upper')
		return function(t) { return t.toUpperCase(); };
	else if(c == 'first')
		return function(t) { return	t.charAt(0).toUpperCase() + t.slice(1).toLowerCase(); };
}

function update() {
	width = Number($('#width').val());
	height = Number($('#height').val());
	rotation = $('#rotation').attr('value').split(',').map(function(d) { return Number(d)*Math.PI/180; } );
	rotation_proba = Number($('#rotation-proba').attr('value'));
	shape = $('#shape').val();
	text_case = case_lookup($('#case').val());
	font = $('#font').val();
	font_scale = scale_lookup($('#font-scale').val());
	font_size = $('#font-size').attr('value').split(',').map(Number);

	if(tags.length)
		draw();
}
$(document).ready(function() {
	$('form').submit(function() {
		// prepare GET url
		var url = window.location.origin+'/view/'+$(this).attr('type');

		data = $(this).serialize();
		if(last_data != data) {
			last_data = data;

			// perform GET request
			$.get(url, data)
			 .done(function(data) {
				tags = JSON.parse(data);
				update();
			});
			// TODO: request error handling
		}
		else
			update();
	});

	$('#save').click(function() {
		// http://stackoverflow.com/questions/23218174/how-do-i-save-export-an-svg-file-after-creating-an-svg-with-d3-js-ie-safari-an
		//get svg source.
		var serializer = new XMLSerializer();
		var source = serializer.serializeToString($('#view').get(0));
		//add name spaces.
		if(!source.match(/^<svg[^>]+xmlns="http\:\/\/www\.w3\.org\/2000\/svg"/)) {
			source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
		}
		if(!source.match(/^<svg[^>]+"http\:\/\/www\.w3\.org\/1999\/xlink"/)) {
			source = source.replace(/^<svg/, '<svg xmlns:xlink="http://www.w3.org/1999/xlink"');
		}
		//add xml declaration
		source = '<?xml version="1.0" standalone="no"?>\r\n' + source;
		//convert svg source to URI data scheme.
		var url = "data:image/svg+xml;charset=utf-8,"+encodeURIComponent(source);
		//open svg
		window.open(url, '_blank');
	});
});
