// Mwatha Maina — Copywriting & Creative Studio
// Progressive enhancement: mobile nav, blog category filtering, footer year, contact form.

(function () {
  "use strict";

  // Mobile navigation toggle
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Blog category filtering
  var filters = document.querySelectorAll("[data-filter]");
  var posts = document.querySelectorAll("[data-category]");
  var noResults = document.querySelector(".no-results");
  if (filters.length && posts.length) {
    filters.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var cat = btn.getAttribute("data-filter");
        filters.forEach(function (b) { b.classList.remove("active"); });
        btn.classList.add("active");

        var visible = 0;
        posts.forEach(function (post) {
          var match = cat === "all" || post.getAttribute("data-category") === cat;
          post.style.display = match ? "" : "none";
          if (match) { visible++; }
        });
        if (noResults) { noResults.style.display = visible ? "none" : "block"; }
      });
    });
  }

  // Footer year
  var yearEl = document.querySelector("[data-year]");
  if (yearEl) { yearEl.textContent = String(new Date().getFullYear()); }

  // Contact form (front-end only — mailto fallback so it works on static hosting)
  var form = document.querySelector("#contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = (form.querySelector("#name") || {}).value || "";
      var email = (form.querySelector("#email") || {}).value || "";
      var project = (form.querySelector("#project") || {}).value || "";
      var message = (form.querySelector("#message") || {}).value || "";
      var subject = encodeURIComponent("Project enquiry — " + (project || "Copywriting"));
      var body = encodeURIComponent(
        "Name: " + name + "\n" +
        "Email: " + email + "\n" +
        "Project type: " + project + "\n\n" +
        message
      );
      window.location.href = "mailto:mwaszac2@gmail.com?subject=" + subject + "&body=" + body;
    });
  }
})();
