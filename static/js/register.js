// record data masukan register
$("#tombol-button-register").click(function () {
  var username_receive = $("#username").val();
  var email_receive = $("#email").val();
  var password_receive = $("#password").val();
  var password2_receive = $("password2").val();

  // statement

  // username
  if (username_receive.length === 0 || username_receive === " ") {
    $("#usernameFeedback")
      .removeClass("valid-feedback")
      .addClass("invalid-feedback")
      .text("username anda masih kosong, Silahkan isi kembali");
    $("#username").removeClass("is-valid").addClass("is-invalid").focus();
    return;
  } else {
    $("#usernameFeedback")
      .removeClass("invalid-feedback")
      .addClass("valid-feedback")
      .text("username anda Benar");
    $("#username").removeClass("is-invalid").addClass("is-valid").focus();
  }
  // end username

  // email
  $("#emailFeedback").removeClass("text-warning");
  if (email_receive.length === 0 || email_receive === " ") {
    $("#emailFeedback")
      .removeClass("valid-feedback")
      .addClass("invalid-feedback")
      .text("email anda masih kosong, Silahkan isi kembali");
    $("#email").removeClass("is-valid").addClass("is-invalid").focus();
    return;
  } else if (!is_email(email_receive)) {
    $("#emailFeedback")
      .removeClass("valid-feedback")
      .addClass("invalid-feedback")
      .text(
        "email anda tidak memenuhi Syarat diantaranya 2-10 aphabet, nomor dan special character -_."
      );
    $("#email").removeClass("is-valid").addClass("is-invalid").focus();
    return;
  } else {
    $("#emailFeedback")
      .removeClass("invalid-feedback")
      .addClass("valid-feedback")
      .text("email anda benar");
    $("#email").removeClass("is-invalid").addClass("is-valid").focus();
  }
  // end email

  // password
  $("#passwordFeedback").removeClass("text-warning");
  if (password_receive.length === 0 || password_receive === " ") {
    $("#passwordFeedback")
      .removeClass("valid-feedback")
      .addClass("invalid-feedback")
      .text("password anda Kosong");
    $("#password").removeClass("is-valid").addClass("is-invalid").focus();
    return;
  } else if (!is_password(password_receive)) {
    $("#passwordFeedback")
      .removeClass("valid-feedback")
      .addClass("invalid-feedback")
      .text(
        "password anda tidak memenuhi Syarat diantara 8-20 aphabet, nomor dan special character !@#$%^&*"
      );
    $("#password").removeClass("is-valid").addClass("is-invalid").focus();
    return;
  } else {
    $("#passwordFeedback")
      .removeClass("invalid-feedback")
      .addClass("valid-feedback")
      .text("password anda benar");
    $("#password").removeClass("is-invalid").addClass("is-valid").focus();
  }
  // end password

  // confirm password
  if (password2_receive.length === 0 || password_receive === " ") {
    $("#password2Feedback")
      .removeClass("valid-feedback")
      .addClass("invalid-feedback")
      .text("confirm password anda masih kosong, Silahkan isi kembali");
    $("#password2").removeClass("is-valid").addClass("is-invalid").focus();
    return;
  } else if (password2_receive !== password_receive) {
    $("#password2Feedback")
      .removeClass("valid-feedback")
      .addClass("invalid-feedback")
      .text("password anda tidak sama");
    $("#password2").removeClass("is-valid").addClass("is-invalid").focus();
    return;
  } else {
    $("#password2Feedback")
      .removeClass("invalid-feedback")
      .addClass("valid-feedback")
      .text("confirm password anda benar");
    $("#password2").removeClass("is-invalid").addClass("is-valid").focus();
  }
  // end confirm password

  // end statement

  var data = {
    username: username,
    email: email,
    password: password,
  };
  $.ajax({
    type: "POST",
    url: "/register/auth",
    data: data,
    success: function (data) {
      if (data["status"] == "success") {
        window.location.href = "/dashboard";
      } else {
        alert(data["message"]);
      }
    },
  });

  // cek email regex
  function is_email(asValue) {
    var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$/;
    return regExp.test(asValue);
  }

  // cek password regex
  function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
  }
});

// tombol register even saat klik enter
$("#form-register").keypress(function (e) {
  console.log(e.key);
  if (e.key === "Enter") {
    $("#tombol-button-register").click();
  }
});