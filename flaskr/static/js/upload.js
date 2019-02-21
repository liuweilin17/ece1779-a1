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
            beforeSend: function() {
                $('#facesDiv').html("<img class='loading' src='static/img/loading.gif'>");
            },
            success: function(data) {
                console.log(data)
                if (data == '') {
                    alert = "<div class='alert alert-danger alert-dismissible fade show' role='alert'>Upload Fail"
                    alert += "<button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span>"
                    alert += "</button></div>"
                    $('#img-alert').html(alert);
                    $('#facesDiv').html('');
                } else {
                    $('#facesDiv').html("<img class='faces-img center' id='facesImg'>");
                    $("#facesImg").attr('src', 'static/images/' + data);
                    alert = "<div class='alert alert-success alert-dismissible fade show text-center' role='alert'>Upload Success"
                    alert += "<button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span>"
                    alert += "</button></div>"
                    $('#img-alert').html(alert);
                }
            },
        });
    }
});

$("#abortBtn").click(function(){
    $('#uploadForm')[0].reset();
    $('#custom-div').html('');
    $('#facesDiv').html('');
    $("#img-size-div").html('');
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
            if (size > 10000) {
                msg = 'The maximum file size is 10MB.'
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
      $('#custom-div').html("<img class='custom-img center' src='" +e.target.result+"'>")
    }
    reader.readAsDataURL(input.files[0]);
    $('#img-size-div').html("<p class='text-center'>"+size+"KB</p>");
  }
}