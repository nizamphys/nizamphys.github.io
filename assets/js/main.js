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

  // Back-to-top button
  var top = document.querySelector(".to-top");
  if (top) {
    var onScroll = function () { top.classList.toggle("is-visible", window.scrollY > 600); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // Highlight the current section in the "On this page" bar
  var subLinks = Array.prototype.slice.call(document.querySelectorAll(".subnav a[href^='#']"));
  if (subLinks.length && "IntersectionObserver" in window) {
    var targets = subLinks.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        subLinks.forEach(function (a) {
          var on = a.getAttribute("href") === "#" + en.target.id;
          a.classList.toggle("is-active", on);
          if (on && a.scrollIntoView && window.innerWidth < 900) {
            a.parentNode.parentNode.scrollLeft = a.parentNode.offsetLeft - 20;
          }
        });
      });
    }, { rootMargin: "-35% 0px -60% 0px" });
    targets.forEach(function (t) { if (t) io.observe(t); });
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
