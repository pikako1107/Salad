$(function () {

    var i = 0;

    // �t�H�[���ǉ�
    document.getElementById("plus").onclick = function () {

        // �C���N�������g
        i++;

        // �e�v�f���擾
        var parent = document.getElementById("detail");

        // �e�v�f�̐擪�ɂ���q�v�f�𕡐��i�R�s�[�j
        var child = parent.firstElementChild.cloneNode(true);
        // id��ύX
        child.id = "form_" + i;

        // �e�v�f�̍Ō���ɕ��������v�f��ǉ�
        parent.appendChild(child); 
    };

    // �t�H�[���폜
    document.getElementById("minus").onclick = function () {

        // �ŏ��̃t�H�[���͏����Ȃ�
        if (i > 0) {
            // �폜�Ώ�
            var delForm = "#form_" + i;
            
            // �폜
            $(delForm).remove();

            // �f�N�������g
            i--;
        }
    };


});