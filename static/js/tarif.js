// // fungsi untuk menambahkan data
// function tambahkanData() {
//   const namaPelanggan = document.getElementById("nama_pelanggan").value;
//   const bulan = document.getElementById("bulan").value;
//   const tahun = document.getElementById("tahun").value;
//   const tanggalCek = document.getElementById("tanggal_cek").value;
//   const meteranAwal = document.getElementById("meteran_awal").value;
//   const meteranAkhir = document.getElementById("meteran_akhir").value;

//   data.push({
//     nama_pelanggan: namaPelanggan,
//     bulan: bulan,
//     tahun: tahun,
//     tanggal_cek: tanggalCek,
//     meteran_awal: meteranAwal,
//     meteran_akhir: meteranAkhir,
//   });

//   tampilkanData();
// }

// // event listener untuk tombol simpan
// document.getElementById("btn-simpan").addEventListener("click", tambahkanData);

// // event listener untuk tombol edit
// document.addEventListener("click", (e) => {
//   if (e.target.classList.contains("btn-edit")) {
//     const index = e.target.dataset.index;
//     editData(index);
//   }
// });

// function hapus data
function hapusdata(userId) {
  $.ajax({
    type: "POST",
    url: "/tarif/delete",
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
