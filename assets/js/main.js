/* Mohammad Nizam — site interactions (no dependencies) */
(function () {
  "use strict";

  // Year in footer
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  // Sticky nav shadow
  var nav = document.querySelector(".nav");
  function onScroll() { nav.classList.toggle("is-scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Mobile menu
  var toggle = document.querySelector(".nav__toggle");
  var menu = document.getElementById("menu");
  toggle.addEventListener("click", function () {
    var open = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!open));
    toggle.setAttribute("aria-label", open ? "Open menu" : "Close menu");
    menu.classList.toggle("is-open", !open);
  });
  menu.addEventListener("click", function (e) {
    if (e.target.tagName === "A") {
      toggle.setAttribute("aria-expanded", "false");
      menu.classList.remove("is-open");
    }
  });

  // Reveal on scroll
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("is-in"); });
  }

  // Active nav link
  var links = Array.prototype.slice.call(document.querySelectorAll(".nav__links a[href^='#']"));
  var sections = links.map(function (a) { return document.querySelector(a.getAttribute("href")); });
  if ("IntersectionObserver" in window) {
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          links.forEach(function (a) { a.classList.toggle("is-active", a.getAttribute("href") === "#" + en.target.id); });
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    sections.forEach(function (s) { if (s) so.observe(s); });
  }

  // Publication filters
  var filters = document.querySelectorAll(".filter");
  var pubs = document.querySelectorAll(".pub");
  filters.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var f = btn.getAttribute("data-filter");
      filters.forEach(function (b) {
        var on = b === btn;
        b.classList.toggle("is-active", on);
        b.setAttribute("aria-pressed", String(on));
      });
      pubs.forEach(function (p) {
        var show = f === "all" || p.getAttribute("data-cat") === f;
        p.classList.toggle("is-hidden", !show);
        if (show) p.classList.add("is-in");
      });
    });
  });

  // Hero background: three interfering "flavour" waves, a nod to neutrino oscillations
  var canvas = document.getElementById("waves");
  if (!canvas || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var ctx = canvas.getContext("2d");
  var w, h, dpr, t = 0, running = true;
  var colors = ["rgba(47,111,214,0.35)", "rgba(217,122,30,0.35)", "rgba(47,158,116,0.28)"];

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = canvas.clientWidth; h = canvas.clientHeight;
    canvas.width = w * dpr; canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function draw() {
    if (!running) return;
    ctx.clearRect(0, 0, w, h);
    var base = h * 0.78;
    for (var k = 0; k < 3; k++) {
      ctx.beginPath();
      ctx.lineWidth = 1.4;
      ctx.strokeStyle = colors[k];
      for (var x = 0; x <= w; x += 4) {
        var phase = (2 * Math.PI * k) / 3;
        // slow envelope (oscillation length) times fast carrier
        var env = Math.cos((x / w) * Math.PI * 1.6 + t * 0.25 + phase);
        var y = base + env * env * 38 * Math.sin(x * 0.018 + t + k);
        if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
    t += 0.012;
    requestAnimationFrame(draw);
  }
  resize();
  window.addEventListener("resize", resize);
  document.addEventListener("visibilitychange", function () {
    running = !document.hidden;
    if (running) requestAnimationFrame(draw);
  });
  requestAnimationFrame(draw);
})();
