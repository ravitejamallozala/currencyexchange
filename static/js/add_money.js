var $DOM = $(document);
$DOM.on('click', '#addmoney-submit', function () {

    console.log("Add money Function");

    data = {};
    data["amount"] = $("#amount").val();
    data["currency_id"] = $("#curr_dropdown").val();
    data["to_user_id"] = $("#to_user").val();
    data["transaction_type"] = "credit";
    data['csrfmiddlewaretoken'] = $("#user1").data('csrf');
    console.log("data: ", data);

    $.ajax({
        type: 'post',
        data: JSON.stringify(data),
        headers: {
            "X-CSRFToken": $("#amount").data('csrf'),
            "content-type": "application/json"
        },
        url: '/api/transaction/wallet_transaction/',

        success: function (result) {
            if (result) {
                alertify.set('notifier', 'position', 'top-right');
                alertify.success('Money Added to Wallet!!!');
                setTimeout(function () {
                    location.reload(true);
                }, 1000);

            } else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.error('Failed to add Money!');
            }

        },
        error: function (request, error) {
            alertify.set('notifier', 'position', 'top-right');
            alertify.error("Failed to add Money!");

        }
    });
});