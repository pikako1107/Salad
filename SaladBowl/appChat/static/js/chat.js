$(function () {
    // �m�F�󋵃N���b�N
    document.getElementById("displayCheck").onclick = function () {
        // display��none��block�֕ύX
        $('#check').css('display', 'block');

        // ���������display��none�֕ύX
        $('#file').css('display', 'none');

        // �}�X�N��\��
        $('#mask').css('display', 'block');
    };
    
    // ���M�t�@�C���N���b�N
    document.getElementById("displayFile").onclick = function () {
        // display��none��block�֕ύX
        $('#file').css('display', 'block');

        // ���������display��none�֕ύX
        $('#check').css('display', 'none');

        // �}�X�N��\��
        $('#mask').css('display', 'block');
    };

    // �}�X�N�N���b�N
    $("#mask").click(function () {

        // display��block��none�֕ύX
        $('#check').css('display', 'none');
        $('#file').css('display', 'none');

        // �}�X�N���\��
        $('#mask').css('display', 'none');
    })

})