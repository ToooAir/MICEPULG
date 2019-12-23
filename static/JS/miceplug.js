window.onload = function (e) {
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    var lineUserId = data.context.userId;
    var path = window.location.pathname

    if(path.indexOf("login")!=-1){
        this.inputSelect();
        this.login(lineUserId);
    }
    else if(path.indexOf("signup")!=-1){
        this.changeupload();
        this.singUp(lineUserId);
    }
    else if(path.indexOf("edit")!=-1){
        this.changeupload();
        this.getProfile(lineUserId);
        this.editprofile(lineUserId);
    }
    else if(path.indexOf("find")!=-1){
        this.sendMessage();
    }
    else if(path.indexOf("comment")!=-1){
        id = getId();
        addComment(lineUserId, id);
    }
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



function preview(input) {
    if (input.files && input.files[0]) {
        for (var i = 0; i < input.files.length; i++) {
            reader = new FileReader();
            reader.readAsDataURL(input.files[i]);
            reader.onload = function (e) {
                var image = new Image();

                image.onload = function () {
                    var canvas = document.createElement("canvas");
                    var context = canvas.getContext("2d");
                    canvas.width = 800;
                    canvas.height = 800 / image.width * image.height;
                    context.drawImage(image,
                        0,
                        0,
                        image.width,
                        image.height,
                        0,
                        0,
                        canvas.width,
                        canvas.height
                    );
                    
                    $("#previewIMG").attr('src', canvas.toDataURL('image/jpeg', 0.8));
                }
                image.src = e.target.result;
            }
        }
    }
}

function changeupload() {
    $("body").on("change", ".upload", function () {
        preview(this);
    })
}



function singUp(lineUserId) {
    $("#send").click(function () {
        if ($("#signUpName").val() != "" && $("#signUpEmail").val() != "" && $("#signUpIntro").val() != "") {

            link = $("#signUpLink").val();
            if (link.indexOf("https://") != -1 || link.indexOf("http://") != -1 || link == "") {
                $(".loading").css("display", "block");

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

                        liff.sendMessages([
                            {
                                type: 'text',
                                text: '我要註冊'
                            }
                        ]).then(function () {
                            liff.closeWindow();
                        }).catch(function (err) {
                            console.log(err);
                            alert('好像出錯了，請聯絡工作人員');
                        })
                    },
                    error: function (jqXHR) {
                        alert(jqXHR.responseText);
                        $("#send").removeAttr("disabled");
                        $(".loading").css("display", "none");
                    }
                });
            } else {
                alert("連結不是正確的");
            };

        } else {
            alert("有必填欄位沒填");
        }

    });
}



function inputSelect() {
    $('#id_no1').focus().select();
    $('#idform').children('div').children('input').keyup(function (e) {
        this.value.length == this.getAttribute('maxlength') && $(this).next().focus();
    });
}

function getDigit() {
    digit = $("#id_no1").val() + $("#id_no2").val() + $("#id_no3").val() + $("#id_no4").val()
    return digit.toUpperCase();
}

function login(lineUserId) {
    $('#signup').click(
        function () {
            window.location.href = "signup";
        }
    )
    $("#login").click(function () {
        var number = getDigit();

        $(".loading").css("display", "block");

        $.ajax({
            type: "POST",
            cache: false,
            data: {
                lineUserId: lineUserId,
                bindId: number
            },
            url: "/bind",
            dataType: "json",
            success: function (data) {
                liff.sendMessages([
                    {
                        type: 'text',
                        text: '#' + number
                    }
                ]).then(function () {
                    liff.closeWindow();
                }).catch(function (err) {
                    console.log(err);
                    alert('好像出錯了，請聯絡工作人員');
                    $(".loading").css("display", "none");
                })

            },
            error: function (jqXHR) {
                alert(jqXHR.responseText);
                $(".loading").css("display", "none");
            }
        });

    });
}



function sendMessage() {
    $("#send").click(function () {
        var Id = $("#findId").val().trim();

        if (Id != "") {
            find = "#" + Id

            $(".loading").css("display", "block");

            liff.sendMessages([
                {
                    type: 'text',
                    text: find
                }
            ]).then(function () {
                $(".loading").css("display", "none");
                liff.closeWindow();
            }).catch(function (err) {
                console.log(err);
                alert('好像出錯了，請聯絡工作人員');
                $(".loading").css("display", "none");

            })

        } else {
            alert("請輸入要查詢對象的個人編號。")
        }

    });
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
                        ]).then(function () {
                            liff.closeWindow();
                        }).catch(function (err) {
                            console.log(err);
                            alert('好像出錯了，請聯絡工作人員');
                            $(".loading").css("display", "none");
                        })
                    },
                    error: function (jqXHR) {
                        alert(jqXHR.responseText);
                        $("#send").removeAttr("disabled");
                        $(".loading").css("display", "none");
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
            $("#previewIMG").attr("src", data["picture"]);


        },
        error: function (jqXHR) {
            alert("error: " + jqXHR.responseText);
        }
    })
}



function addComment(lineUserId, id) {
    $("#send").click(function () {
        var msg = $('#comment').val().trim();

        if (msg != "") {
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