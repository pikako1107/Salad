$(function () {
    // �쐬�t�H�[���\��
    document.getElementById("createBtn").onclick = function () {
        // �\���N���X�ǉ�
        $("#createForm").addClass("indication");
        maskToggle();
    };

    // �폜�t�H�[���\��
    document.getElementById("deleteBtn").onclick = function () {
        // �\���N���X�ǉ�
        $("#deleteForm").addClass("indication");
        maskToggle();
    };

    // �t�H�[���̖߂�{�^���N���b�N
    $('.return').click(function () {
        deleteForm();
    })

    // �}�X�N�N���b�N
    $("#mask").click(function () {
        deleteForm();
    })

    // �t�H�[���폜����
    function deleteForm() {
        // �e�v�f���擾
        var parent = $('.return').parent();

        // �\���N���X���폜
        parent.removeClass("indication");
        maskToggle();
    }

    // �}�X�N����֐�
    function maskToggle() {
        // �}�X�N�̔�\���E�\������ւ�
        $("#mask").toggle();
    }

})