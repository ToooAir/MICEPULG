$(document).ready(function () {
	function preview(input) {
		if (input.files && input.files[0]) {
			for (var i = 0; i < input.files.length; i++) {
				reader = new FileReader();
				reader.readAsDataURL(input.files[i]);
				reader.onload = function (e) {
					var image = new Image();

					image.onload = function () {
						var canvas = document.createElement("canvas");
						var context = canvas.getContext("2d");
						canvas.width = 800;
						canvas.height = 800/image.width*image.height;
						context.drawImage(image,
							0,
							0,
							image.width,
							image.height,
							0,
							0,
							canvas.width,
							canvas.height
						);
						var img = document.getElementById("previewIMG");
						img.setAttribute('src', canvas.toDataURL('image/jpeg', 0.8));
					}
					image.src = e.target.result;
				}
			}
		}
	}
	$("body").on("change", ".upload", function () {
		preview(this);
	})
})	