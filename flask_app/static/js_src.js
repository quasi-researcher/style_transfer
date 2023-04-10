function update_label() {
    var out_img = document.getElementById('out_img');
    const image_content = document.getElementById('selected_c_image').files[0];
    const image_style = document.getElementById('selected_s_image').files[0];
    var formData = new FormData();
    formData.append('content', image_content);
    formData.append('style', image_style);
    $.ajax({
        url: "/generate",
        type: "POST",
        processData: false,
        contentType: false,
        data: formData,
        beforeSend: function() {
            $('#loading').append("<img id='load' src='static/process.gif' width='128' height='128' />");
            $("#file_missed").css('visibility','hidden');
        },
        success: function(data) {
                if (!data['error']) {
                    $("#file_missed").css('visibility','hidden');
                    out_img.src = 'data:image/png;base64, ' + data.out_img;
                    }
                else {

                        $("#file_missed").css('visibility','visible');
                    }
                $('#load').remove();

            },
        error: function(error) {
            console.log('${error}');
        }

    });

}