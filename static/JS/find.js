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

        if(Id != "") {
            find = "#" + Id

            $(".loading").css("display", "block");

            liff.sendMessages([
                {
                type:'text',
                text:find
                }
            ]).then(function(){
                $(".loading").css("display", "none");
                liff.closeWindow();
            }).catch(function(err){
                console.log(err);
                alert('好像出錯了，請聯絡工作人員');
                $(".loading").css("display", "none");

            })
            
        } else {
            alert("請輸入要查詢對象的個人編號。")
        }
        
    });
}