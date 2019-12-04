window.onload = function (e) {
    var lineUserId = "lol";
    this.singUp(lineUserId);

    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    var lineUserId = data.context.userId;
}

function singUp(lineUserId) {
    $("#send").click(function () {
        data = new FormData($("#signupForm")[0]);
        data.append("lineUserId", lineUserId);
        window.alert(lineUserId);
        $.ajax({
            type: "POST",
            cache: false,
            data: data,
            url: "/register",
            dataType: "formData",
            processData: false,
            contentType: false,
            success: function (data) {
                alert(data);
            },
            error: function (jqXHR) {
                alert("error: " + jqXHR.responseText);
            }
        })
    });
}