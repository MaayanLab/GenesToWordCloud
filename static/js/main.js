$(document).ready(function() {
	$(".dropdown-button").dropdown();
	$(".button-collapse").sideNav();
	$('select').material_select();

	$.each($('.noUiSlider'), function() {
		var elem = $(this);
		// create range slider
		noUiSlider.create(this, {
			start: eval(elem.attr('start')),
			connect: eval(elem.attr('connect')) || 'lower',
			step: eval(elem.attr('step')) || 1,
			range: {
				'min': eval(elem.attr('min')) || 0,
				'max': eval(elem.attr('max')) || 100
			},
			format: wNumb({
				decimals: eval(elem.attr('fmt')) || 0
			})
		});
		this.noUiSlider.on('set', function(value) {
			elem.attr('value', value);
		});
		// set start value (force event fire)
		this.noUiSlider.set(eval(elem.attr('start')));
	});
});
