$(document).ready(function(){
	//
	$(".fancy").click(function(){
			var uid=this.getAttribute("data-id");
			//ajax
			var request = $.ajax({
				url: "ajax/",
				type: "GET",
				data: {
					type: "fancy",
					id: uid
				},
				dataType: "json"
			});

			request.done(function(msg) {
				console.log(msg.status);
				if(msg.status == 0){

				}
			});

			request.fail(function(jqXHR, textStatus) {
				alert( "Request failed: " + textStatus );
			});
		}
	);
});