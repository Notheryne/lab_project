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
        url: 'http://127.0.0.1:5000/api/users',
        datatype: 'json',
        crossDomain: true,
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(msg) {
            // location.href = msg['goto'];
        }
    })
}

function sendFormLogin(ev) {
    ev.preventDefault();
    var data = getFormData($("#login-form"));
    console.log(data);
    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/api/users/login',
        datatype: 'json',
        data: JSON.stringify(data),
        crossDomain: true,
        contentType: 'application/json',
        success: function(msg) {
            // location.href = this.url;
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
