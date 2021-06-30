var $DOM = $(document);
$DOM.on('click', '#profile-submit', function () {

    console.log("Profile Function");
    user = $("#profile-image").data('user');
    var formData = new FormData();
    var pimage = $("#customFile")[0].files[0]
    if (pimage) {
        formData.append("profile_image", $("#customFile")[0].files[0]);
    }
    formData.append("currency_id", $("#curr_dropdown").val());
    console.log("Profile Function");


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
                console.log("Add money Successed");
                 alertify.message('Profile data updated');
                alertify.set('notifier', 'position', 'top-right');
            } else {
                console.log("Add money  Failed");
                alertify.error(result.message);
            }
        }
    });
});