$(function () {
    // �쐬�t�H�[���\��
    document.getElementById("createBtn").onclick = function () {
        // �\���N���X�ǉ�
        $("#createForm").addClass("indication");
    };

    // �폜�t�H�[���\��
    document.getElementById("deleteBtn").onclick = function () {
        // �\���N���X�ǉ�
        $("#deleteForm").addClass("indication");
    };

    // �t�H�[���̖߂�{�^���N���b�N
    $('.return').click(function () {
        // �e�v�f���擾
        var parent = $('.return').parent();

        // �\���N���X���폜
        parent.removeClass("indication");
    })

})