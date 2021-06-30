var $DOM = $(document);
$DOM.on('click', '#login_submit', function () {
    data = {};
    data["username"] = $("#id_username").val();
    data["password"] = $("#id_password").val();
    console.log(" Her in login")
    $.ajax({
        type: 'post',
        data: JSON.stringify(data),
        headers: {
            "X-CSRFToken": $("#id_username").data('csrf'),
            "content-type": "application/json"
        },
        url: '/login/',

        success: function (result) {
            if (result) {
                alertify.set('notifier', 'position', 'top-right');
                alertify.success('Login Sucessfull!!!');
                setTimeout(function () {
                    location.replace("/");
                }, 1000);
            } else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.error("Login Failed, Incorrect Credentials!");
            }
        },
        error: function (request, error) {
            alertify.set('notifier', 'position', 'top-right');
            alertify.error("Login Failed, Incorrect Credentials!");

        }

    });
});