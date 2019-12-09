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
        data = new FormData($("#editForm")[0]);
        data.append("lineUserId", lineUserId);
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
                      type:'text',
                      text:'修改成功'
                    }
                  ]);
                liff.closeWindow();
            },
            error: function (jqXHR) {
                alert("error: " + jqXHR.responseText);
            }
        });
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
            $("#previewIMG").attr("src","/static/uploadImage/"+data["picture"]);
        },
        error: function (jqXHR) {
            alert("error: " + jqXHR.responseText);
        }
    })
}