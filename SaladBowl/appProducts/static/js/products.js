$(function () {
    $('input[name=select]').change(function () {
        // 選択されたラジオボタンを格納
        var result = $('input[name=select]:checked').val();

        // 検索が選択された場合
        if (result === 'search') {
            // 登録フォームを非表示
            $('.input_form').hide();
            // 検索フォームを表示
            $('.search_form').show();
        } else {
            // 検索フォームを非表示
            $('.search_form').hide();
            // 登録フォームを表示
            $('.input_form').show();
        }
    });
});