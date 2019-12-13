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

            liff.sendMessages([
                {
                type:'text',
                text:find
                }
            ]).then(function(){
                liff.closeWindow();
            }).catch(function(err){
                console.log(err);
                alert('好像出錯了，請聯絡工作人員');
            })
            
        } else {
            alert("請輸入要查詢對象的個人編號。")
        }
        
    });
}