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
        window.alert(lineUserId);
        $.ajax({
            type: "POST",
            cache: false,
            data: data,
            url: "/editprofile",
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

function getProfile(lineUserId) {
    $.ajax({
        type: "POST",
        cache: false,
        data: {
            lineUserId: lineUserId,
        },
        url: "/getprofile",
        dataType: "json",
        success: function (response) {
            $("#editName").val(response["name"]);
            $("#editEmail").val(response["email"]);
            $("#editIntro").val(response["intro"]);
            $("#editLink").val(response["link"]);
        },
        error: function (jqXHR) {
            alert("error: " + jqXHR.responseText);
        }
    })
}