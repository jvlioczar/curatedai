/* Curated AI · interactions: smooth scroll, reveals, cursor, glow, filters, rail */
(function () {
  "use strict";
  var doc = document.documentElement;
  if (!doc.classList.contains("js")) doc.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  /* ---------- superbar scrolls away: keep fixed elements below it while it is visible ---------- */
  var bar = document.getElementById("bvbar"), barH = bar ? bar.offsetHeight : 0;
  function barVis() { doc.style.setProperty("--bar-vis", Math.max(0, barH - (window.scrollY || 0)) + "px"); }
  barVis();
  window.addEventListener("scroll", barVis, { passive: true });
  window.addEventListener("resize", function () { barH = bar ? bar.offsetHeight : 0; barVis(); });

  /* ---------- smooth scroll (Lenis) ---------- */
  var lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new Lenis({ lerp: 0.09, wheelMultiplier: 1, smoothWheel: true });
    function raf(t) { lenis.raf(t); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener("click", function (ev) {
        var id = a.getAttribute("href");
        var el = id.length > 1 && document.querySelector(id);
        if (!el) return;
        ev.preventDefault();
        lenis.scrollTo(el, { offset: -80, duration: 1.4 });
        history.pushState(null, "", id);
      });
    });
  }

  /* ---------- film transition between pages ---------- */
  if (!reduce) {
    document.addEventListener("click", function (ev) {
      if (ev.defaultPrevented || ev.button !== 0 || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
      var a = ev.target.closest("a[href]");
      if (!a || a.target === "_blank" || a.hasAttribute("download") || a.getAttribute("href").charAt(0) === "#") return;
      var url;
      try { url = new URL(a.href, location.href); } catch (e) { return; }
      if (url.origin !== location.origin || url.protocol !== location.protocol) return;
      if (url.pathname === location.pathname && url.search === location.search && url.hash) return;
      ev.preventDefault();
      doc.classList.add("leaving");
      setTimeout(function () { location.href = url.href; }, 520);
    });
    window.addEventListener("pageshow", function (ev) { if (ev.persisted) doc.classList.remove("leaving"); });
  }

  /* ---------- scroll reveals ---------- */
  var revealables = document.querySelectorAll(".reveal, .card, .cat-tile, .crit, .deg");
  if (reduce || !("IntersectionObserver" in window)) {
    revealables.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        var sib = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
        el.style.transitionDelay = Math.min(sib % 6, 5) * 70 + "ms";
        el.classList.add("in");
        io.unobserve(el);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    setTimeout(function () { revealables.forEach(function (el) { io.observe(el); }); }, 250);
  }

  /* ---------- marquee follows the scroll direction ---------- */
  var marquee = document.querySelector(".marquee-track");
  if (marquee && !reduce) {
    var lastY = window.scrollY || 0, dir = 1;
    window.addEventListener("scroll", function () {
      var y = window.scrollY || 0, d = y > lastY ? 1 : (y < lastY ? -1 : dir);
      lastY = y;
      if (d !== dir) { dir = d; marquee.style.animationDirection = d === 1 ? "normal" : "reverse"; }
    }, { passive: true });
  }

  /* ---------- 3D tilt on cards ---------- */
  if (fine && !reduce) {
    document.querySelectorAll(".card, .cat-tile").forEach(function (card) {
      var raf = null;
      card.addEventListener("pointermove", function (ev) {
        var r = card.getBoundingClientRect();
        var x = (ev.clientX - r.left) / r.width - 0.5, y = (ev.clientY - r.top) / r.height - 0.5;
        if (raf) cancelAnimationFrame(raf);
        raf = requestAnimationFrame(function () {
          card.style.transform = "perspective(900px) rotateX(" + (-y * 6).toFixed(2) + "deg) rotateY(" + (x * 8).toFixed(2) + "deg) translateY(-4px)";
        });
      });
      card.addEventListener("pointerleave", function () { if (raf) cancelAnimationFrame(raf); card.style.transform = ""; });
    });
  }

  /* ---------- cursor trail: blurred dots lagging behind the pointer ---------- */
  var cur = document.getElementById("cursor");
  if (fine && !reduce && cur) {
    doc.classList.add("has-cursor");
    var dots = Array.prototype.slice.call(cur.querySelectorAll(".tr")), dot = cur.querySelector(".cur-dot");
    var pts = dots.map(function () { return { x: innerWidth / 2, y: innerHeight / 2 }; });
    var mx = innerWidth / 2, my = innerHeight / 2, visible = false;
    dots.forEach(function (d, i) {
      var k = 1 - i / dots.length;
      d.style.width = d.style.height = (6 + 16 * k).toFixed(1) + "px";
      d.style.opacity = (0.15 + 0.5 * k).toFixed(2);
    });
    window.addEventListener("pointermove", function (ev) {
      mx = ev.clientX; my = ev.clientY;
      if (dot) dot.style.transform = "translate(" + mx + "px," + my + "px)";
      if (!visible) { visible = true; cur.style.opacity = "1"; }
    }, { passive: true });
    document.addEventListener("pointerover", function (ev) { cur.classList.toggle("is-link", !!ev.target.closest("a, button, [data-cursor]")); });
    window.addEventListener("pointerdown", function () { cur.classList.add("is-down"); });
    window.addEventListener("pointerup", function () { cur.classList.remove("is-down"); });
    document.addEventListener("pointerleave", function () { cur.style.opacity = "0"; visible = false; });
    (function loop() {
      var tx = mx, ty = my;
      pts.forEach(function (p, i) {
        var f = 0.35 - i * 0.035;
        p.x += (tx - p.x) * f; p.y += (ty - p.y) * f;
        dots[i].style.transform = "translate(" + p.x.toFixed(1) + "px," + p.y.toFixed(1) + "px) translate(-50%,-50%)";
        tx = p.x; ty = p.y;
      });
      requestAnimationFrame(loop);
    })();
  }

  /* ---------- rail: collapse toggle + fluid highlight ---------- */
  var rail = document.getElementById("rail"), toggle = document.getElementById("railToggle"), hl = document.getElementById("railHl");
  if (toggle) {
    function label(min) { toggle.setAttribute("aria-expanded", String(!min)); toggle.setAttribute("aria-label", toggle.getAttribute(min ? "data-expand" : "data-collapse")); }
    label(doc.classList.contains("rail-min"));
    toggle.addEventListener("click", function () {
      var min = doc.classList.toggle("rail-min");
      label(min);
      try { localStorage.setItem("rail", min ? "min" : "max"); } catch (e) {}
    });
  }
  if (rail && hl && fine && !reduce) {
    var hy = 0, hh = 0, ty = 0, th = 0, hot = false;
    function target(el) {
      var r = el.getBoundingClientRect(), rr = rail.getBoundingClientRect();
      ty = r.top - rr.top; th = r.height;
      var h = el.style.getPropertyValue("--h");
      hl.style.setProperty("--hh", h || "20");
      if (!hot) { hy = ty; hh = th; hot = true; hl.style.transform = "translateY(" + hy + "px)"; hl.style.height = hh + "px"; hl.classList.add("on"); }
    }
    rail.addEventListener("pointerover", function (ev) {
      var a = ev.target.closest(".rail-cats a, .rail-nav a");
      if (a) target(a);
    });
    rail.addEventListener("pointerleave", function () { hot = false; hl.classList.remove("on"); });
    (function loop() {
      if (hot) {
        hy += (ty - hy) * 0.18; hh += (th - hh) * 0.18;
        hl.style.transform = "translateY(" + hy.toFixed(1) + "px)";
        hl.style.height = hh.toFixed(1) + "px";
      }
      requestAnimationFrame(loop);
    })();
  }

  /* ---------- rail drawer (mobile) ---------- */
  var btn = document.getElementById("menuBtn"), scrim = document.getElementById("scrim");
  function setRail(open) {
    if (!rail) return;
    rail.classList.toggle("open", open);
    if (scrim) scrim.classList.toggle("open", open);
    if (btn) btn.setAttribute("aria-expanded", String(open));
    document.body.style.overflow = open ? "hidden" : "";
    if (lenis) open ? lenis.stop() : lenis.start();
  }
  if (btn) btn.addEventListener("click", function () { setRail(!rail.classList.contains("open")); });
  if (scrim) scrim.addEventListener("click", function () { setRail(false); });
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") setRail(false); });

  /* ---------- sort (category pages) ---------- */
  var sortBox = document.getElementById("sort"), catGrid = document.getElementById("catgrid");
  if (sortBox && catGrid) {
    var key = function (el) { return el.getAttribute("data-title").toLowerCase().replace(/^(the|an|a|o|os|as|um|uma)\s+/, ""); };
    var byTitle = function (a, b) { return key(a).localeCompare(key(b), undefined, { sensitivity: "base", ignorePunctuation: true }); };
    var modes = {
      az: byTitle,
      old: function (a, b) { return (+a.getAttribute("data-year") - +b.getAttribute("data-year")) || byTitle(a, b); },
      "new": function (a, b) { return (+b.getAttribute("data-year") - +a.getAttribute("data-year")) || byTitle(a, b); }
    };
    sortBox.addEventListener("click", function (ev) {
      var b = ev.target.closest(".fchip");
      if (!b || b.getAttribute("aria-pressed") === "true") return;
      var mode = b.getAttribute("data-s");
      sortBox.querySelectorAll(".fchip").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      var items = Array.prototype.slice.call(catGrid.querySelectorAll(".card")).sort(modes[mode]);
      items.forEach(function (c, i) { c.classList.add("in"); c.style.transitionDelay = "0ms"; catGrid.appendChild(c); });
      try { history.replaceState(null, "", mode === "az" ? location.pathname : "?sort=" + mode); } catch (e) {}
    });
    var want = new URLSearchParams(location.search).get("sort"), pre = want && sortBox.querySelector('.fchip[data-s="' + want + '"]');
    if (pre) pre.click();
  }

  /* ---------- filters (home) ---------- */
  var filters = document.getElementById("filters"), grid = document.getElementById("allgrid");
  if (filters && grid) {
    var active = { purpose: null, degree: null };
    var cards = Array.prototype.slice.call(grid.querySelectorAll(".card"));
    var clear = document.getElementById("fclear"), empty = document.getElementById("fempty");
    function apply() {
      var n = 0;
      cards.forEach(function (c) {
        var ok = (!active.purpose || (" " + c.getAttribute("data-purposes") + " ").indexOf(" " + active.purpose + " ") >= 0) &&
                 (!active.degree || c.getAttribute("data-degree") === active.degree);
        c.classList.toggle("is-hidden", !ok);
        if (ok) { n++; c.classList.add("in"); }
      });
      filters.querySelectorAll(".fchip").forEach(function (b) { b.setAttribute("aria-pressed", String(active[b.getAttribute("data-f")] === b.getAttribute("data-v"))); });
      var any = !!(active.purpose || active.degree);
      if (clear) clear.hidden = !any;
      if (empty) empty.hidden = n > 0;
    }
    filters.addEventListener("click", function (ev) {
      var b = ev.target.closest(".fchip");
      if (!b) return;
      var f = b.getAttribute("data-f"), v = b.getAttribute("data-v");
      active[f] = active[f] === v ? null : v;
      apply();
    });
    if (clear) clear.addEventListener("click", function () { active = { purpose: null, degree: null }; apply(); });
    var q = new URLSearchParams(location.search);
    if (q.get("purpose")) active.purpose = q.get("purpose");
    if (q.get("degree")) active.degree = q.get("degree");
    if (active.purpose || active.degree) apply();
  }
})();
