$(function () {

    // �ǂݍ��ݎ��̏���
    window.onload = function () {
        changeForm();
    }

    // ���W�I�{�^���ύX����
    $('input[name=select]').change(function () {
        changeForm();
    });

    // �t�H�[������ւ�
    function changeForm() {
        // �I�����ꂽ���W�I�{�^�����i�[
        var result = $('input[name=select]:checked').val();

        // �������I�����ꂽ�ꍇ
        if (result === 'search') {
            // �o�^�t�H�[�����\��
            $('.input_form').hide();
            // �����t�H�[����\��
            $('.search_form').show();
        } else {
            // �����t�H�[�����\��
            $('.search_form').hide();
            // �o�^�t�H�[����\��
            $('.input_form').show();
        }
    }
});