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
        var Id = $("#findId").val().trim();

        if(id != "") {
            find = "#" + Id

            liff.sendMessages([
                {
                type:'text',
                text:find
                }
            ])

            liff.closeWindow();
        } else {
            alert("請輸入要查詢對象的個人編號。")
        }
        
    });
}