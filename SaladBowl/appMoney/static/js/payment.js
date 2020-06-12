$(function () {

    var i = 1;

    // フォーム追加
    document.getElementById("plus").onclick = function () {

        // 親要素を取得
        let parent = document.getElementById("detail");

        // 親要素の先頭にある子要素を複製（コピー）
        let child = parent.firstElementChild.cloneNode(true);
        // idを変更
        child.id = "form_" + i;

        // 親要素の最後尾に複製した要素を追加
        parent.appendChild(child); 

        // インクリメント
        i++;
    };


});