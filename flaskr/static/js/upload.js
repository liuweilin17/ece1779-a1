$(document).ready(function() {
    $('#nav-upload').siblings().removeClass('active');
    $('#nav-upload').addClass('active');
    $('#uploadForm').submit(function(e) {
        e.preventDefault();
    });
});
$('#customFile').on('change',function(){
    if (checkImg(this)) {
        previewImg(this)
        $('#customImg').show()
    }
})
$("#uploadBtn").click(function(){
    input = $('#customFile')[0]
    if (checkImg(input)) {
        var form_data = new FormData($('#uploadForm')[0]);
        $.ajax({
            type: 'POST',
            url: 'uploadImage',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                $("#facesImg").attr('src', 'static/images/' + data);
                $("#facesImg").show()
                $("#customImg").hide()
                $("#img-size").html('Upload Success!')
            },
        });
    }
});

$("#abortBtn").click(function(){
    $('#uploadForm')[0].reset();
    $('#customImg').hide();
    $('#facesImg').hide();
    $("#img-size").hide();
    $("#img-alert").html('');
    $('#customFile').next('.custom-file-label').html('Choose your files');
});

function checkImg(input) {
    valid = false
    msg = ''
    if (input.files && input.files[0]) {
        $('#customFile').next('.custom-file-label').html(input.files[0].name);
        if (input.files.length > 1) {
            msg = 'You should only choose one file at a time.'
        } else {
            var size = Math.round(input.files[0].size/1000)
            var type = input.files[0].type
            if (size > 500) {
                msg = 'The maximum file size is 500kB.'
            } else if ($.inArray(input.files[0].type, ['image/jpeg', 'image/jpg', 'image/png']) == -1) {
                msg = 'Valid file type is image/jpeg, image/jpg or image/png.'
            } else {
                valid = true
            }
        }
    }
    else {
        msg = 'You should choose a image before upload.'
    }
    if (! valid) {
        alert = "<div class='alert alert-danger alert-dismissible fade show' role='alert'>" + msg
        alert += "<button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span>"
        alert += "</button></div>"
        console.log(alert)
        $('#img-alert').html(alert);
    }

    return valid
}

function previewImg(input) {
  if (input.files && input.files[0]) {
    var fileName = input.files[0].name;
    var size = Math.round(input.files[0].size / 1000)
    $('#customFile').next('.custom-file-label').html(fileName);
    var reader = new FileReader();
    reader.onload = function(e) {
      $('#customImg').attr('src', e.target.result);
    }
    reader.readAsDataURL(input.files[0]);
    $('#img-size').html(size+'KB');
    $('#img-size').show();
  }
}