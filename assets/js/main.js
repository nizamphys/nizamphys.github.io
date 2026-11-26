/* Dr. Mohammad Nizam — site interactions (no dependencies) */
(function () {
  "use strict";

  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  // Mobile menu
  var toggle = document.querySelector(".nav__toggle");
  var nav = document.getElementById("nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      toggle.textContent = open ? "Menu" : "Close";
      nav.classList.toggle("is-open", !open);
    });
  }

  // Publication filters
  var filters = document.querySelectorAll(".filter");
  if (!filters.length) return;
  var pubs = document.querySelectorAll(".pub");
  var groups = document.querySelectorAll(".year-group");
  var count = document.querySelector(".pub-count");

  function apply(f) {
    var shown = 0;
    pubs.forEach(function (p) {
      var match = f === "all" || p.dataset.theme === f || p.dataset.type === f;
      p.classList.toggle("is-hidden", !match);
      if (match) shown++;
    });
    groups.forEach(function (g) {
      g.classList.toggle("is-empty", !g.querySelector(".pub:not(.is-hidden)"));
    });
    if (count) count.textContent = shown + (shown === 1 ? " record" : " records");
  }

  filters.forEach(function (btn) {
    btn.addEventListener("click", function () {
      filters.forEach(function (b) {
        var on = b === btn;
        b.classList.toggle("is-active", on);
        b.setAttribute("aria-pressed", String(on));
      });
      apply(btn.dataset.filter);
    });
  });
  apply("all");
})();
