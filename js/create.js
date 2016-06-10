// Create a word cloud with d3-cloud with keyword results from server

var d3 = require('d3');
var cloud = require('d3-cloud');

var fill = d3.scale.category20();

// Create the cloud with default options
var layout = cloud()
	.padding(5)
	.fontSize(function(d) { return d.size; })
	.on('end', draw);

function draw(words) {
	// redraw the cloud layout

	$('#view').empty();
	d3.select($('#view').get(0))
	  .append('svg')
		.attr('width', layout.size()[0])
		.attr('height', layout.size()[1])
	  .append('g')
		.attr('transform', 'translate(' + layout.size()[0] / 2 + ',' + layout.size()[1] / 2 + ')')
	  .selectAll('text')
		.data(words)
		.enter()
	  .append('text')
		.style('font-size', layout.fontSize())
		.style('font-family', layout.font())
		.style('fill', function(d, i) { return fill(i); })
		.attr('text-anchor', 'middle')
		.attr('transform', function(d) {
			return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')';
		})
		.text(function(d) { return d.text; });
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

$(document).ready(function() {
	$('form').submit(function() {
		// load layout with new layout options

		// canvas size
		var width = Number($(this).find('#width').val()),
			height = Number($(this).find('#height').val());

		// font
		var font = $(this).find('#font').val();

		// font size
		var font_size = $('#font-size').attr('value').split(',').map(Number);

		// TODO: $(this).find('#placer'), layout.spiral

		// set new layout options
		layout.stop()
			  .size([width, height])
			  .rotate(angler_lookup($(this).find('#angler').val()))
			  .font(font)
			  .fontSize(function(d) {
				return (d.size*(font_size[1]-font_size[0])+font_size[0])+'px';
			   });

		// prepare GET url
		var url = window.location.origin+'/view/'+$(this).attr('type');

		// perform GET request
		$.get(url, $(this).serialize())
		 .done(function(data) {
			data = JSON.parse(data); // parse the data
			layout.words(data['words'].map(function(d) { // convert words dict to javascript object
				return {text: d['text'], size: (d['freq']/data['max'])}
			})).start(); // start new layout

			// warn user if d3-cloud didn't display all the text (which it does sometimes)
			if($('#view').find('text').length < layout.words().length)
				$('#view').append('<p>Note: Not all words could be displayed, make the canvas bigger.</p>');
		});
		// TODO: error handling
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

	layout.start(); // display the layout
});
