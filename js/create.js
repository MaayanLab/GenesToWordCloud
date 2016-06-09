var d3 = require('d3');
var cloud = require('d3-cloud');

var fill = d3.scale.category20();
var layout = cloud()
	.padding(5)
	.fontSize(function(d) { return d.size; })
	.on("end", draw);

layout.start();

function draw(words) {
	$("#view").empty();
	d3.select($("#view").get(0))
	  .append("svg")
		.attr("width", layout.size()[0])
		.attr("height", layout.size()[1])
	  .append("g")
		.attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
	  .selectAll("text")
		.data(words)
		.enter()
	  .append("text")
		.style("font-size", function(d) { return d.size + "px"; })
		.style("font-family", "Impact")
		.style("fill", function(d, i) { return fill(i); })
		.attr("text-anchor", "middle")
		.attr("transform", function(d) {
			return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
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
			layout.words(JSON.parse(data).map(function(d) {
				return {text: d['text'], size: d['size']}
			})).start();
		});
		// TODO: error handling
	});
});
