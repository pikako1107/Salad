$(function () {

    var i = 0;

    // フォーム追加
    document.getElementById("plus").onclick = function () {

        // インクリメント
        i++;

        // 親要素を取得
        var parent = document.getElementById("detail");

        // 親要素の先頭にある子要素を複製（コピー）
        var child = parent.firstElementChild.cloneNode(true);
        // idを変更
        child.id = "form_" + i;

        // 親要素の最後尾に複製した要素を追加
        parent.appendChild(child); 
    };

    // フォーム削除
    document.getElementById("minus").onclick = function () {

        // 最初のフォームは消さない
        if (i > 0) {
            // 削除対象
            var delForm = "#form_" + i;
            
            // 削除
            $(delForm).remove();

            // デクリメント
            i--;
        }
    };


});