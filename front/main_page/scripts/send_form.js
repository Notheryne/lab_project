function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

function SendFormRegister() {
    var data = getFormData($("#login-form"));
    console.log(data);
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/api/users',
        datatype: 'json',
        crossDomain: true,
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(msg) {
            location.href = msg['goto'];
        }
    })
}

function SendFormLogin() {
    var data = getFormData($("#login-form"));
    console.log(data);
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/api/users',
        datatype: 'json',
        data: JSON.stringify(data),
        crossDomain: true,
        contentType: 'application/json',
        success: function(msg) {
            location.href = this.url;
        }
    })
}

