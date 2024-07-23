$(function () {
  // record data masukan login
  $("#tombol-button-login").click(function () {
    var email = $("#email").val();
    var password = $("#password").val();
    var data = {
      email: email,
      password: password,
    };
    $.ajax({
      type: "POST",
      url: "/login/auth",
      data: data,
      success: function (data) {
        if (data["status"] == "success") {
          window.location.href = "/dashboard";
        } else {
          alert(data["message"]);
        }
      },
    });
  });

  // tombol login even saat klik enter
  $("#form-login").keypress(function (e) {
    if (e.key === "Enter") {
      $("#tombol-button-login").click();
    }
  });
});
