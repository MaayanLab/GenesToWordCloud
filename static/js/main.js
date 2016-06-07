function create(url) {
	$('#view').html('<img src="/view/'+url+'?'+$('form').serialize()+'" />');
}

$(document).ready(function() {
	$(".dropdown-button").dropdown();
	$(".button-collapse").sideNav();
    $('select').material_select();
});
