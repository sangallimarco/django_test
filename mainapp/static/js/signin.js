$(document).ready(function(){
	$('#insertform').validate({
		rules: {
			"name": {
				minlength: 2,
				required: true
			},
			"surname": {
				minlength: 2,
				required: true
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

});