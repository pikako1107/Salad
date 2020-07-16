$(function () {
    // 作成フォーム表示
    document.getElementById("createBtn").onclick = function () {
        // 表示クラス追加
        $("#createForm").addClass("indication");
        maskToggle();
    };

    // 削除フォーム表示
    document.getElementById("deleteBtn").onclick = function () {
        // 表示クラス追加
        $("#deleteForm").addClass("indication");
        maskToggle();
    };

    // フォームの戻るボタンクリック
    $('.return').click(function () {
        deleteForm();
    })

    // マスククリック
    $("#mask").click(function () {
        deleteForm();
    })

    // フォーム削除処理
    function deleteForm() {
        // 親要素を取得
        var parent = $('.return').parent();

        // 表示クラスを削除
        parent.removeClass("indication");
        maskToggle();
    }

    // マスク操作関数
    function maskToggle() {
        // マスクの非表示・表示入れ替え
        $("#mask").toggle();
    }

})