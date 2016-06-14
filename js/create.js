// Create a word cloud with d3-cloud with keyword results from server
// https://github.com/shprink/d3js-wordcloud

// Imports
var d3 = require('d3');
var cloud = require('d3-cloud');

// Properties
var width = 960;
var height = 600;
var angler, spiral;
var font, font_scale, font_size;
var text_case, tags = [];


var fill = d3.scale.category20b();
var last_data, fontSize;

var layout = cloud()
	.timeInterval(Infinity)
	.size([width, height])
	.fontSize(function(d) {
	    return fontSize(+d.value);
	})
	.text(function(d) {
	    return d.key;
	})
	.on("end", draw);

var svg = d3.select("#view").append("svg")
    .attr("width", width)
    .attr("height", height);

var vis = svg.append("g").attr("transform", "translate(" + [width >> 1, height >> 1] + ")");

function draw(data, bounds) {
	var w = width,
	    h = height;

	svg.attr("width", w).attr("height", h);

	scale = bounds ? Math.min(
	        w / Math.abs(bounds[1].x - w / 2),
	        w / Math.abs(bounds[0].x - w / 2),
	        h / Math.abs(bounds[1].y - h / 2),
	        h / Math.abs(bounds[0].y - h / 2)) / 2 : 1;

	var text = vis.selectAll("text")
	        .data(data, function(d) {
	            return d.text;
	        });
	text.transition()
	        .duration(1000)
	        .attr("transform", function(d) {
	            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
	        })
	        .style("font-size", function(d) {
	            return d.size + "px";
	        });
	text.enter().append("text")
	        .attr("text-anchor", "middle")
	        .attr("transform", function(d) {
	            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
	        })
	        .style("font-size", function(d) {
	            return d.size + "px";
	        })
	        .style("opacity", 1e-6)
	        .transition()
	        .duration(1000)
	        .style("opacity", 1);
	text.style("font-family", function(d) {
	    return d.font;
	})
	        .style("fill", function(d) {
	            return fill(text_case(d.text));
	        })
	        .text(function(d) {
	            return text_case(d.text);
	        });

	vis.transition().attr("transform", "translate(" + [w >> 1, h >> 1] + ")scale(" + scale + ")");
}

function angler_lookup(angler) {
	// return the rotation function for a specific angler option

	if(angler == 'mostlyHoriz')
		return function() { return (~~(Math.random() * 6) - 3) * 30; };
	else if(angler == 'hexes')
		return function() { return ~~(Math.random() * 2) * 45; };
	else if(angler == 'heaped')
		return function() { return ~~(Math.random() * 2) * 90; };
	else if(angler == 'horiz')
		return 0;
	else if(angler == 'updAndDown')
		return 90;
	else if(angler == 'random')
		return function() { return Math.random() * 360; };
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
	angler = angler_lookup($('#angler').val());
	spiral = $('#spiral').val();
	text_case = case_lookup($('#case').val());
	font = $('#font').val();
	font_scale = $('#font-scale').val();
	font_size = $('#font-size').attr('value').split(',').map(Number);

    layout.font(font).spiral('archimedean');
    fontSize = d3.scale[font_scale]().range([font_size[0], font_size[1]]);
    if(tags.length)
        fontSize.domain([+tags[tags.length - 1].value || 1, +tags[0].value]);
    layout.stop().words(tags).start();
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
				tags = JSON.parse(data).map(function(d) { // convert words dict to javascript object tags
					return {key: d['text'], value: d['freq']};
				});
				update();
			});
			// TODO: error handling
		}
		else
			update();
	});

	$('#save').click(function() {
		// http://stackoverflow.com/questions/23218174/how-do-i-save-export-an-svg-file-after-creating-an-svg-with-d3-js-ie-safari-an
		//get svg element.
		var svg = $('#view').find('svg').get(0);
		//get svg source.
		var serializer = new XMLSerializer();
		var source = serializer.serializeToString(svg);
		//add name spaces.
		if(!source.match(/^<svg[^>]+xmlns="http\:\/\/www\.w3\.org\/2000\/svg"/)){
			source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
		}
		if(!source.match(/^<svg[^>]+"http\:\/\/www\.w3\.org\/1999\/xlink"/)){
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
