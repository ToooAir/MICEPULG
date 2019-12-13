window.onload = function (e) {
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    var lineUserId = data.context.userId;
    id = getId();
    addComment(lineUserId, id);
}

function addComment(lineUserId, id) {
    $("#send").click(function () {
        var msg = $('#comment').val().trim();

        if(msg != "") {
            data = {
                lineUserId: lineUserId,
                id: id,
                comment: msg,
            };

            $(".loading").css("display", "block");
    
            $.ajax({
                type: "POST",
                cache: false,
                data: data,
                url: "/addcomment",
                dataType: "json",
                success: function (data) {
                    location.reload();
                },
                error: function (jqXHR) {
                    alert(jqXHR.responseText);
                    $(".loading").css("display", "none");
                }
            });
        } else {
            alert("請填寫留言內容。")
        }

    });

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
        return id;
    }
}