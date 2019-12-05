window.onload = function (e) {
    liff.init(function (data) {
        initializeApp(data);
    });
};

function initializeApp(data) {
    sendMessage();
}

function sendMessage() {
    $("#send").click(function () {
        var Id = $("#findId").val();
        find = "我要找#" + Id + "號"
        liff.sendMessages([
            {
              type:'text',
              text:find
            }
          ])
        liff.closeWindow();
    });
}