$(document).ready(function(){
	$('#loginform').validate({
		rules: {
			"user": {
				minlength: 2,
				required: true
			},
			"password": {
				minlength: 2,
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
