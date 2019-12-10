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
        find = "#" + Id
        liff.sendMessages([
            {
              type:'text',
              text:find
            }
          ])
        liff.closeWindow();
    });
}