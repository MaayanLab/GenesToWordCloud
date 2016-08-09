var view = $('#view');
var state = $('#status');

// Properties
var width = 960;
var height = 600;
var rotation, rotation_proba, shape, grid_size;
var font, font_scale, font_size;
var text_case, tags = [], tags_left, threshold;
var max_freq;
var last_data, fontSize;

function draw() {
	view.height(height * view.width() / width);
	view[0].setAttribute('viewBox', '0 0 '+width+' '+height);
	var filtered_tags = tags.filter(function(t) {
		return t[1] > threshold;
	}).map(function(t) {
		return [text_case(t[0]), t[1]]
	});
	tags_left = filtered_tags.map(function(t) { return t[0]; });
	WordCloud(view[0], {
		width: width,
		height: height,
		shuffle: true,
		backgroundColor: 'rgba(255, 255, 255, 0)',
		list: filtered_tags,
		fontFamily: font,
		gridSize: grid_size,
		weightFactor: function (size) { return font_size[0] + Math.pow(size / max_freq, font_scale) * (font_size[1] - font_size[0]); },
		rotateRatio: rotation_proba,
		minRotation: rotation[0],
		maxRotation: rotation[1],
		shape: shape
	});
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
	grid_size = Number($('#grid-size').attr('value'));
	text_case = case_lookup($('#case').val());
	font = $('#font').val();
	font_scale = Number($('#font-scale').attr('value'));
	font_size = $('#font-size').attr('value').split(',').map(Number);
	threshold = Number($('#threshold').attr('value'));

	if(tags.length)
		draw();
}
$(document).ready(function() {
	$(window).resize(function() { view.height(height * view.width() / width); });
	$('form').submit(function() {
		// prepare GET url
		var url = window.location.origin+'/view/'+$(this).attr('type');

		data = $(this).serialize();
		if(last_data != data) {
			last_data = data;

			// perform GET request
			state.text("Processing...");
			$.get(url, data)
			 .done(function(data) {
				tags = JSON.parse(data);
				max_freq = Math.max.apply(Math, tags.map(function(d) { return d[1]; }));
			}).fail(function() {
				state.text("Couldn't communicate with server");
			}).done(function() {
				state.text("");
				update();
			});
		}
		else
			update();
	});

	view.on('wordcloudstart', function() {
		state.text("Generating Wordcloud...");
	});

	view.on('wordclouddrawn', function(e) {
		var d = e.originalEvent.detail;
		if(d.drawn)
			tags_left.splice(tags_left.indexOf(d.item[0]), 1);
	});

	view.on('wordcloudstop', function() {
		if(tags_left.length > 0)
			state.text("NOTE: "+ tags_left.length + " word(s) were unable to be placed, try adjusting settings so you don't miss them.");
		else
			state.text("");
	});

	$('#save').click(function() {
		// modified from http://stackoverflow.com/questions/23218174/how-do-i-save-export-an-svg-file-after-creating-an-svg-with-d3-js-ie-safari-an

		var serializer = new XMLSerializer();
		var source = serializer.serializeToString($('#view').get(0));

		if(!source.match(/^<svg[^>]+xmlns="http\:\/\/www\.w3\.org\/2000\/svg"/)) {
			source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
		}
		if(!source.match(/^<svg[^>]+"http\:\/\/www\.w3\.org\/1999\/xlink"/)) {
			source = source.replace(/^<svg/, '<svg xmlns:xlink="http://www.w3.org/1999/xlink"');
		}
		if(source.match(/^<svg[^>]+style="/)) {
			source = source.replace(/style="[^"]+"/, '');
		}
		source = '<?xml version="1.0" standalone="no"?>\r\n' + source;
		var url = "data:image/svg+xml;charset=utf-8,"+encodeURIComponent(source);
		window.open(url, '_blank');
	});
});
