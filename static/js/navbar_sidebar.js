$(document).ready(function () {
  // handle sidebar saat toogle
  header_toogle = $("#header-toggle");
  side_bar = $("#side-bar");
  body_pd = $("#body-pd");
  header_pd = $("#header");

  //   validate that variable all exist
  if (header_toogle && side_bar && body_pd && header_pd) {
    header_toogle.click(function () {
      // showNavbar
      side_bar.toggleClass("show-toggle");
      //   changeIcon
      header_toogle.toggleClass("bx-x");
      // add padding to body
      body_pd.toggleClass("body-pd");
      // add padding to header
      header_pd.toggleClass("body-pd");
    });
  }
  //   end

  /*===== LINK ACTIVE =====*/
  const linkcolor = document.querySelectorAll(".nav_link");
  const title = $("title").text().split("|")[0].trim();

  for (const link of linkcolor) {
    if (link.textContent.trim() == title) {
      $(link).addClass("active");
    }
  }

  /*===== END =====*/
});
