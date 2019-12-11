window.onload = function (e) {
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    var lineUserId = data.context.userId;
    this.singUp(lineUserId);
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

function singUp(lineUserId) {
    $("#send").click(function () {
        if ($("#signUpName").val() != "" && $("#signUpEmail").val() != "" && $("#signUpIntro").val() != "") {
            $(".loading").css("display", "block");
            
            link = $("#signUpLink").val();
            if (link.indexOf("https://") != -1 || link.indexOf("http://") != -1 || link == "") {
                data = new FormData($("#signupForm")[0]);
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
                    url: "/register",
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        liff.closeWindow();
                    },
                    error: function (jqXHR) {
                        alert(jqXHR.responseText);
                        $("#send").removeAttr("disabled");
                    }
                });
            } else {
                alert("連結不是正確的");
            };

        }else{
            alert("有必填欄位沒填");
        }

    });
}