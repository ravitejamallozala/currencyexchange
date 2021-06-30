var $DOM = $(document);
$DOM.on('click', '#withdraw-submit', function () {
    data = {};
    data["amount"] = $("#amount").val();
    data["currency_id"] = $("#curr_dropdown").val();
    data["to_user_id"] = $("#to_user").val();
    data["transaction_type"] = "debit";
    $.ajax({
        type: 'post',
        data: JSON.stringify(data),
        url: '/api/transaction/wallet_transaction/',
        headers: {
            "X-CSRFToken": $("#amount").data('csrf'),
            "content-type": "application/json"
        },
        success: function (result) {
            if (result) {
                alertify.set('notifier', 'position', 'top-right');
                alertify.success('Withdraw Succesfull!!!');
                setTimeout(function () {
                    location.reload(true);
                }, 1000);

            } else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.error('Failed to withdraw Money!');
            }
        },
        error: function (request, error) {
            alertify.set('notifier', 'position', 'top-right');
            alertify.error("Sorry! Failed due to Insuffecient balance.");

        }
    });
});