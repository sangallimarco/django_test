$(document).ready(function(){
	$('#insertform').validate({
		rules: {
			"username": {
				minlength: 2,
				required: true
			},
			"name": {
				minlength: 2,
				required: true
			},
			"email": {
				required: true,
				email: true
			},
			"surname": {
				minlength: 2,
				required: true,
			},
			"phone": {
				required: true,
				tel: true
			},
			"tags": {
				required: true
			},
			"groups": {
				required: true
			}
		},
		highlight: function(label) {
			$(label).closest('.control-group').removeClass('success').addClass('error');
			console.log('error');
		},
		success: function(label) {
			$(label).closest('.control-group').removeClass('error').addClass('success');
		}
	});

	//token JS
	$("#id_tags").tokenInput("ajax/",
		{
			theme: "facebook",
			preventDuplicates:true
		}
	);

});