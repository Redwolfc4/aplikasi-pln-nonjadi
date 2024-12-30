var nama = $("#text-profile").text().trim(``);

$("#text-profile").click(function () {
  window.location.href = `/info_akun?nama=${nama}`;
});
