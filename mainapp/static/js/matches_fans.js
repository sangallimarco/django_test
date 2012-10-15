$(document).ready(function () {
	//
	$(".accept").click(function () {
			var uid = this.getAttribute("data-id");
			var ref = this;
			//ajax
			var request = $.ajax({
				url:"../ajax/",
				type:"GET",
				data:{
					type:"accept",
					id:uid
				},
				dataType:"json"
			});

			request.done(function (msg) {
				//$(ref).parents(".thumbnail").css('opacity', "0.3");
				$(ref).remove();
			});

			request.fail(function (jqXHR, textStatus) {
				alert("Request failed: " + textStatus);
			});
		}
	);
	//
	$(".dismiss").click(function () {
			var uid = this.getAttribute("data-id");
			var ref = this;
			//ajax
			var request = $.ajax({
				url:"../ajax/",
				type:"GET",
				data:{
					type:"dismiss",
					id:uid
				},
				dataType:"json"
			});

			request.done(function (msg) {
				//$(ref).parents(".thumbnail").css('opacity', "0.1");
				$(ref).remove();
			});

			request.fail(function (jqXHR, textStatus) {
				alert("Request failed: " + textStatus);
			});
		}
	);
});