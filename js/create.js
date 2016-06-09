var d3 = require('d3');
var cloud = require('d3-cloud');

var fill = d3.scale.category20();
var layout = cloud()
	.padding(5)
	.fontSize(function(d) { return d.size; })
	.on('end', draw);

layout.start();

function draw(words) {
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
		.style('font-size', function(d) { return d.size + 'px'; })
		.style('font-family', 'Impact')
		.style('fill', function(d, i) { return fill(i); })
		.attr('text-anchor', 'middle')
		.attr('transform', function(d) {
			return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')';
		})
		.text(function(d) { return d.text; });
}

function angler_lookup(angler) {
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
		layout.stop()
			  .size([Number($(this).find('#width').val()),
					 Number($(this).find('#height').val())])
			  .rotate(angler_lookup($(this).find('#angler').val()))
			  .font('Impact');
		// layout.font()
		// $(this).find('#placer')
		// layout.fontSize
		// layout.spiral

		var url = $(this).attr('type');
		$.get(window.location.origin+'/view/'+url, $(this).serialize())
		 .done(function(data) {
		 	data = JSON.parse(data);
			layout.words(data['words'].map(function(d) {
				return {text: d['text'], size: (d['freq']/data['max'])*24}
			})).start();
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
});
