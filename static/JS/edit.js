window.onload = function (e) {
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    var lineUserId = data.context.userId;
    this.getProfile(lineUserId);
    this.editprofile(lineUserId);
}

function editprofile(lineUserId) {
    $("#send").click(function () {
        if ($("#editName").val() != "") {
            link = $("#editLink").val();
            if (link.indexOf("https://") != -1 || link.indexOf("http://") != -1) {
                data = new FormData($("#editForm")[0]);
                data.append("lineUserId", lineUserId);
                $("#send").attr("disabled", "disabled");
                $.ajax({
                    type: "POST",
                    cache: false,
                    data: data,
                    url: "/editprofile",
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        liff.sendMessages([
                            {
                                type: 'text',
                                text: '修改成功'
                            }
                        ]);
                        liff.closeWindow();
                    },
                    error: function (jqXHR) {
                        alert("error: " + jqXHR.responseText);
                        $("#send").removeAttr("disabled");
                    }
                });

            } else {
                alert("連結不是正確的");
            }

        } else {
            alert("姓名不能為空");
        }


    });
}

function getProfile(lineUserId) {
    $.ajax({
        type: "POST",
        cache: false,
        data: {
            lineUserId: lineUserId,
        },
        url: "/getprofile",
        dataType: "json",
        success: function (data) {
            $("#editName").val(data["name"]);
            $("#editEmail").val(data["email"]);
            $("#editJob").val(data["job"]);
            $("#editIntro").val(data["intro"]);
            $("#editLink").val(data["link"]);
            $("#editTag1").val(data["tag1"]);
            $("#editTag2").val(data["tag2"]);
            $("#editTag3").val(data["tag3"]);
            $("#previewIMG").attr("src", "/static/uploadImage/" + data["picture"]);
        },
        error: function (jqXHR) {
            alert("error: " + jqXHR.responseText);
        }
    })
}