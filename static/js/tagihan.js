// function hapus data
function hapusdata(userId) {
  $.ajax({
    type: "POST",
    url: "/meteran/delete",
    data: { deleteuserId_receive: userId },
    success: function (response) {
      if (response.result === "success") {
        // Muat ulang halaman setelah menghapus data user
        alert(response.msg);
        location.reload();
      } else {
        alert("Gagal menghapus data user: " + response.msg);
      }
    },
    error: function (error) {
      alert("Terjadi kesalahan saat menghapus tarif");
    },
  });
}

// event listener untuk tombol hapus
document.addEventListener("click", (e) => {
  if (e.target.classList.contains("btn-danger")) {
    const index = e.target.dataset.id;
    hapusdata(index);
  }
});

// listern select change
$("#status").change(function () {
  $(this).form.submit();
});
