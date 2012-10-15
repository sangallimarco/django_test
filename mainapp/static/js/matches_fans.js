$(document).ready(function(){
	//
	$(".accept").click(function(){
			var uid=this.getAttribute("data-id");
			//ajax
			var request = $.ajax({
				url: "../ajax/",
				type: "GET",
				data: {
					type: "accept",
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
	//
	$(".dismiss").click(function(){
			var uid=this.getAttribute("data-id");
			//ajax
			var request = $.ajax({
				url: "../ajax/",
				type: "GET",
				data: {
						type: "dismiss",
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