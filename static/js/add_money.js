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
        url: '/transaction/wallet_transaction/',

        success: function (result) {
            console.log(result);
            if (result.success) {
                console.log("Add money Successed");
            } else {
                console.log("Add money  Failed");
                alertify.set('notifier', 'position', 'top-right');
                alertify.error(result.message);
            }
        }
    });
});