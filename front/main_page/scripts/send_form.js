function getFormData($form){
    const unindexed_array = $form.serializeArray();
    let indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

function sendFormRegister(ev) {
    ev.preventDefault();
    var data = getFormData($("#login-form"));
    console.log(data);
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/api/register',
        datatype: 'json',
        crossDomain: true,
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(msg) {
            if (msg['success'] === true) {
                location.href = msg['redirect_url'];
            } else {
                let status_label = document.getElementById('server-message');
                status_label.innerHTML = msg['message'];
            }
        }
    })
}

function sendFormLogin(ev) {
    ev.preventDefault();
    var data = getFormData($("#login-form"));
    // console.log(data);
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/api/login',
        datatype: 'json',
        data: JSON.stringify(data),
        crossDomain: true,
        contentType: 'application/json',
        success: function(msg) {
            if (msg['success'] === true) {
                window.localStorage.setItem('access_token', msg['access_token']);
                window.localStorage.setItem('refresh_token', msg['refresh_token']);
                location.href = msg['redirect_url'];
            } else {
                let status_label = document.getElementById('server-message');
                status_label.innerHTML = msg['message'];
            }
        }
    })
}
window.onload = () => {
  const loginSubmitButton = document.getElementById('login-submit');
  const registerSubmitButton = document.getElementById('register-submit');

  if (loginSubmitButton) {
      loginSubmitButton.addEventListener('click', sendFormLogin);
  }

  if (registerSubmitButton) {
      registerSubmitButton.addEventListener('click', sendFormRegister);
  }
};
