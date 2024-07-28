// fungsi untuk menampilkan data
function tampilkanData() {
  const tbody = document.getElementById("tbody-data");
  tbody.innerHTML = "";
  data.forEach((item, index) => {
    const row = document.createElement("tr");
    row.innerHTML = `
        <td>${item.nama_pelanggan}</td>
        <td>${item.bulan}</td>
        <td>${item.tahun}</td>
        <td>${item.tanggal_cek}</td>
        <td>${item.meteran_awal}</td>
        <td>${item.meteran_akhir}</td>
        <td>
          <button class="btn-hapus" data-index="${index}">Hapus</button>
        </td>
      `;
    tbody.appendChild(row);
  });
}

// fungsi untuk menambahkan data
function tambahkanData() {
  const namaPelanggan = document.getElementById("nama_pelanggan").value;
  const bulan = document.getElementById("bulan").value;
  const tahun = document.getElementById("tahun").value;
  const tanggalCek = document.getElementById("tanggal_cek").value;
  const meteranAwal = document.getElementById("meteran_awal").value;
  const meteranAkhir = document.getElementById("meteran_akhir").value;

  data.push({
    nama_pelanggan: namaPelanggan,
    bulan: bulan,
    tahun: tahun,
    tanggal_cek: tanggalCek,
    meteran_awal: meteranAwal,
    meteran_akhir: meteranAkhir,
  });

  tampilkanData();
}

// fungsi untuk menghapus data
function hapusData(index) {
  data.splice(index, 1);
  tampilkanData();
}

// event listener untuk tombol simpan
document.getElementById("btn-simpan").addEventListener("click", tambahkanData);

// event listener untuk tombol edit
document.addEventListener("click", (e) => {
  if (e.target.classList.contains("btn-edit")) {
    const index = e.target.dataset.index;
    editData(index);
  }
});

// event listener untuk tombol hapus
document.addEventListener("click", (e) => {
  if (e.target.classList.contains("btn-hapus")) {
    const index = e.target.dataset.index;
    hapusData(index);
  }
});
