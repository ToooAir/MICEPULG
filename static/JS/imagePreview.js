$(document).ready(function () {
	function preview(input) {
		if (input.files && input.files[0]) {
			for(var i=0;i<input.files.length;i++) {
				reader = new FileReader();
				reader.onload = function (e) {						
					var img = document.getElementById("previewIMG");
					img.setAttribute('src',e.target.result);
				}
				reader.readAsDataURL(input.files[i]);
			}
		}
	}
	$("body").on("change", ".upload", function () {
		preview(this);
	})
})	