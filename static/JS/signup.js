window.onload = function (e) {
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    var lineUserId = data.context.userId;
    this.singUp(lineUserId);
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
                liff.closeWindow();
            },
            error: function (jqXHR) {
                alert("error: " + jqXHR.responseText);
            }
        });
    });
}