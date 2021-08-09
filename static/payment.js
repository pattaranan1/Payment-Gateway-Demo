function checkStatus() {
    $.ajax({
        url: "/check-status",
        headers: { "user": user , "user_code": user_code},
        type: "GET",
    }).done((response) => {
        console.log(response['status']);
        if (response['status'] === 'success') {
            window.location = response['redirect_page'];
        }
    }).fail((error) =>{
        console.log(error);
    });
    }
    setInterval(() => {
        checkStatus();
        console.log(user);
    }, 5000);