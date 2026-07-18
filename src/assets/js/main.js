// Prowriters101 — Copywriting & Creative Studio (THA_011)
//
// Progressive enhancement, on purpose: the site is fully readable with zero
// JavaScript (all posts render server-side; the form degrades to a plain
// mailto). This file only *improves* the experience -- nav, filtering, a live
// year and a friendlier contact hand-off. Every block guards its own elements,
// so one missing feature never breaks the rest of the page.

(function () {
  "use strict";

  // --- Mobile navigation -------------------------------------------------
  // Toggle the menu and keep aria-expanded honest for screen readers.
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // --- Blog category filter ----------------------------------------------
  // Show/hide cards client-side. No reload, no server -- just fast filtering.
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

  // --- Footer year -------------------------------------------------------
  // Set once at load so the copyright never silently goes stale.
  var yearEl = document.querySelector("[data-year]");
  if (yearEl) { yearEl.textContent = String(new Date().getFullYear()); }

  // --- Contact form ------------------------------------------------------
  // No backend by design: we compose a pre-filled mailto so the site stays a
  // pure static deploy. The recipient comes from data-email (set from
  // config.yaml) so the address lives in exactly one place.
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
      var recipient = form.getAttribute("data-email") || "Prowriters101@gmail.com";
      window.location.href = "mailto:" + recipient + "?subject=" + subject + "&body=" + body;
    });
  }
})();
