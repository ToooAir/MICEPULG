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
        if ($("#signUpName").val() != "") {
            link = $("#signUpLink").val();
            if (link.indexOf("https://") != -1 || link.indexOf("http://") != -1) {
                data = new FormData($("#signupForm")[0]);
                data.append("lineUserId", lineUserId);
                $("#send").attr("disabled", "disabled");
                $.ajax({
                    type: "POST",
                    cache: false,
                    data: data,
                    url: "/register",
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        liff.closeWindow();
                    },
                    error: function (jqXHR) {
                        alert("error: " + jqXHR.responseText);
                        $("#send").removeAttr("disabled");
                    }
                });
            } else {
                alert("連結不是正確的");
            };

        }else{
            alert("姓名不能為空");
        }

    });
}