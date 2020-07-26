$(function () {
    // 確認状況クリック
    document.getElementById("displayCheck").onclick = function () {
        // displayをnone→blockへ変更
        $('#check').css('display', 'block');

        // もう一方のdisplayをnoneへ変更
        $('#file').css('display', 'none');

        // マスクを表示
        $('#mask').css('display', 'block');
    };
    
    // 送信ファイルクリック
    document.getElementById("displayFile").onclick = function () {
        // displayをnone→blockへ変更
        $('#file').css('display', 'block');

        // もう一方のdisplayをnoneへ変更
        $('#check').css('display', 'none');

        // マスクを表示
        $('#mask').css('display', 'block');
    };

    // マスククリック
    $("#mask").click(function () {

        // displayをblock→noneへ変更
        $('#check').css('display', 'none');
        $('#file').css('display', 'none');

        // マスクを非表示
        $('#mask').css('display', 'none');
    })

})