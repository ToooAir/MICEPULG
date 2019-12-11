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
        const input = $('#comment').val();
        data = {
            lineUserId: lineUserId,
            id: id,
            comment: input,
        };
        $.ajax({
            type: "POST",
            cache: false,
            data: data,
            url: "/addcomment",
            dataType: "json",
            success: function (data) {
                // name = data["name"];
                // time = data["time"];
                // const result = "<div><label>" + name + " " + time + " " + input + "</label></div >";
                // $('#comment').val('');
                // $('#comment_list').append(result);
                location.reload();
            },
            error: function (jqXHR) {
                alert(jqXHR.responseText);
            }
        });

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