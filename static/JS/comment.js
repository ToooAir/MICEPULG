window.onload = function (e) {
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
}

function getId() {
	let url = location.href;
	if (url.indexOf('?') != -1) {
		let id = "";

		let ary = url.split('?')[1].split('&');
		for (i = 0; i < ary.length; i++) {
			if (ary[i].split('=')[0] == 'id') {
				id = ary[i].split('=')[1];
			}
		}
		// document.getElementById("app-redeem").style.backgroundImage = `url('https://mcdapp1.azureedge.net/${id}.jpg')`;
	}
}
