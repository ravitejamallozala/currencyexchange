var $DOM = $(document);
$DOM.on('click', '#transfer-submit', function () {

    console.log("submit clicked");
    data = {};
    data["amount"] = $("#amount").val();
    data["currency_id"] = $("#curr_dropdown").val();
    data["from_user_id"] = $("#user1").data('id');
    data["to_user_id"] = $("#to_user").val();
    console.log("data: ", data);

    $.ajax({
        type: 'post',
        data: JSON.stringify(data),
        headers: {
            "X-CSRFToken": $("#user1").data('csrf'),
            "content-type": "application/json"
        },
        url: '/api/transaction/transfer_money/',

        success: function (result) {
            if (result) {
                alertify.set('notifier', 'position', 'top-right');
                alertify.success('Money Transfered!!!');
                setTimeout(function () {
                    location.reload(true);
                }, 1000);
            } else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.error("Failed Money Trasnfered!!!");
            }
        }
    });
});