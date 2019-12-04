window.onload = function (e) {
    this.inputSelect();
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    // todo:liff close window
    var lineUserId = data.context.userId;
    this.login(lineUserId);
}

function inputSelect() {
    $('#id_no1').focus().select();
    $('#idform').children('input').keyup(function (e) {
        // 限制只能輸入數字
        if (!/^\d+$/.test(this.value)) {
            var newValue = /^\d+/.exec(this.value);
            newValue != null ? $(this).val(newValue) : $(this).val('');
        }
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
                alert(data);
            },
            error: function (jqXHR) {
                alert("error: " + jqXHR.responseText);
            }
        })
    });
}

function getDigit() {
    digit = $("#id_no1").val() + $("#id_no2").val() + $("#id_no3").val() + $("#id_no4").val()
    return digit;
}


$('#signup').click(
    function () {
        window.location.href = "signup";
    }
)