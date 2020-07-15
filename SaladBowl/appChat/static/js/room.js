$(function () {
    // 作成フォーム表示
    document.getElementById("createBtn").onclick = function () {
        // 表示クラス追加
        $("#createForm").addClass("indication");
    };

    // 削除フォーム表示
    document.getElementById("deleteBtn").onclick = function () {
        // 表示クラス追加
        $("#deleteForm").addClass("indication");
    };

    // フォームの戻るボタンクリック
    $('.return').click(function () {
        // 親要素を取得
        var parent = $('.return').parent();

        // 表示クラスを削除
        parent.removeClass("indication");
    })

})