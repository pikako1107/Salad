$(function () {

    var i = 1;

    // �t�H�[���ǉ�
    document.getElementById("plus").onclick = function () {

        // �e�v�f���擾
        let parent = document.getElementById("detail");

        // �e�v�f�̐擪�ɂ���q�v�f�𕡐��i�R�s�[�j
        let child = parent.firstElementChild.cloneNode(true);
        // id��ύX
        child.id = "form_" + i;

        // �e�v�f�̍Ō���ɕ��������v�f��ǉ�
        parent.appendChild(child); 

        // �C���N�������g
        i++;
    };


});