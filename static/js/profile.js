var $DOM = $(document);
$DOM.on('click', '#profile-submit', function () {

    console.log("Profile Function");
    user = $("#profile-image").data('user');
    var formData = new FormData();
    var pimage = $("#customFile")[0].files[0];
    if (pimage) {
        formData.append("profile_image", $("#customFile")[0].files[0]);
    }
    formData.append("default_currency", $("#curr_dropdown").val());
    console.log("Profile Function", formData);


    $.ajax({
        type: 'patch',
        data: formData,
        url: '/api/user/' + user + "/",
        contentType: false,
        processData: false,
        headers: {
            "X-CSRFToken": $("#profile-image").data('csrf'),
        },
        success: function (result) {
            if (result) {
                alertify.message('Profile Updated!!!');
                alertify.set('notifier', 'position', 'top-right');
                setTimeout(function () {
                    location.reload(true);
                }, 1000);
                console.log("Profile Updation Successful");
            } else {
                console.log("Profile Updation  Failed");
                alertify.error(result.message);
            }
        }
    });
});