window.onload = function (e) {
    lineUserId = "U80652db48632d5c313b01e447b79510c";
    this.getProfile(lineUserId);
    this.editprofile(lineUserId);
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    var lineUserId = data.context.userId;
    this.getProfile(lineUserId);
    this.editprofile(lineUserId);
}

function dataURItoBlob(dataURI) {
    var byteString = atob(dataURI.split(',')[1]);
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0]
    var ab = new ArrayBuffer(byteString.length);
    var ia = new Uint8Array(ab);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    var blob = new Blob([ab], { type: mimeString });
    return blob;
}

function editprofile(lineUserId) {
    $("#send").click(function () {
        if ($("#editName").val() != "" && $("#editEmail").val() != "" && $("#editIntro").val() != "") {

            link = $("#editLink").val();
            if (link.indexOf("https://") != -1 || link.indexOf("http://") != -1 || link == "") {
                $(".loading").css("display", "block");
                data = new FormData($("#editForm")[0]);
                data.append("lineUserId", lineUserId);
                var uri = $("#previewIMG").attr("src");
                if (uri.indexOf("http") == -1 && uri.indexOf("uploadImage") == -1) {
                    var imgBlob = dataURItoBlob(uri);
                    data.append("image", imgBlob, "image.jpg");
                }
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
                        alert(jqXHR.responseText);
                        $("#send").removeAttr("disabled");
                    }
                });

            } else {
                alert("連結不是正確的");
            }

        } else {
            alert("有必填欄位沒填");
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
            if(data["picture"].indexOf("http")==-1){
                $("#previewIMG").attr("src", "/static/uploadImage/" + data["picture"]);
            }else{
                $("#previewIMG").attr("src", data["picture"]);
            }
            
        },
        error: function (jqXHR) {
            alert("error: " + jqXHR.responseText);
        }
    })
}

