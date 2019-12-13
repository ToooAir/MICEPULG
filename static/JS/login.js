window.onload = function (e) {
    this.inputSelect();
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    var lineUserId = data.context.userId;
    this.login(lineUserId);
}

function inputSelect() {
    $('#id_no1').focus().select();
    $('#idform').children('div').children('input').keyup(function (e) {
        this.value.length == this.getAttribute('maxlength') && $(this).next().focus();
    });
}

function login(lineUserId) {
    $("#login").click(function () {
        var number = getDigit();
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
                    type:'text',
                    text:'#' + number
                    }
                ]).then(function(){
                    liff.closeWindow();
                }).catch(function(err){
                    console.log(err);
                    alert('好像出錯了，請聯絡工作人員');
                })
                
            },
            error: function (jqXHR) {
                alert(jqXHR.responseText);
            }
        });

    });
}

function getDigit() {
    digit = $("#id_no1").val() + $("#id_no2").val() + $("#id_no3").val() + $("#id_no4").val()
    return digit.toUpperCase();
}


$('#signup').click(
    function () {
        window.location.href = "signup";
    }
)