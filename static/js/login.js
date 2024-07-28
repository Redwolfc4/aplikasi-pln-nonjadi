$(function () {
  // record data masukan login
  $("#tombol-button-login").click(function () {
    var email = $("#email").val();
    var password = $("#password").val();
    var data = {
      email_give: email,
      password_give: password,
    };
    $.ajax({
      type: "POST",
      url: "/login/auth",
      data: data,
      success: function (data) {
        if (data["result"] == "success") {
          $.cookie(data.token_key, data.token, { path: "/" });
          alert(data.msg);
          window.location.replace("/");
        } else {
          alert(data["msg"]);
          window.location.reload();
        }
      },
    });
  });
  // end record
});
// tombol login even saat klik enter
$("#form-login").keypress(function (e) {
  if (e.key === "Enter") {
    $("#tombol-button-login").click();
  }
});
// end login eveb enter
