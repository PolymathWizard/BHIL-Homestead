/*
  HOMESTEAD safety layer, script, v1.0.0
  Modern by design and exempt from the era lint (ADR-003).

  What it does:
    - Adds a Safe Mode toggle as the first focusable element on the page.
    - Safe Mode pauses animated GIFs (swaps src to data-still), stops every
      marquee, stops blink emulation, stops audio, and raises contrast.
    - Safe Mode starts on when the visitor prefers reduced motion, and the
      choice is remembered per browser when storage is available.
    - Click-to-play audio for any element with data-hs-audio="file.wav".
      Nothing ever plays without a click (WCAG 1.4.2).
    - Exposes window.homesteadSafe() so period scripts (cursor trails, text
      scrollers) can pause themselves.

  Do not edit copies; the drift gate compares every copy with kits/safety-layer/.
*/
(function () {
  "use strict";

  var KEY = "homestead-safe-mode";
  var doc = document;
  var root = doc.documentElement;
  var toggle = null;
  var live = null;
  var players = [];

  function readStored() {
    try {
      return window.localStorage.getItem(KEY);
    } catch (e) {
      return null;
    }
  }

  function writeStored(value) {
    try {
      window.localStorage.setItem(KEY, value);
    } catch (e) {
      /* storage blocked; the choice lasts for this page view only */
    }
  }

  function prefersReducedMotion() {
    return !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  }

  function isSafe() {
    return root.className.indexOf("hs-safe") !== -1;
  }

  function announce(message) {
    if (live) {
      live.textContent = "";
      window.setTimeout(function () { live.textContent = message; }, 30);
    }
  }

  function setPressed(el, on) {
    el.setAttribute("aria-pressed", on ? "true" : "false");
  }

  function stopAllAudio() {
    for (var i = 0; i < players.length; i++) {
      players[i].audio.pause();
      players[i].audio.currentTime = 0;
      setPressed(players[i].el, false);
    }
  }

  function swapImages(safe) {
    var imgs = doc.querySelectorAll("img[data-still]");
    for (var i = 0; i < imgs.length; i++) {
      var img = imgs[i];
      if (safe) {
        if (!img.getAttribute("data-anim")) {
          img.setAttribute("data-anim", img.getAttribute("src"));
        }
        img.setAttribute("src", img.getAttribute("data-still"));
      } else if (img.getAttribute("data-anim")) {
        img.setAttribute("src", img.getAttribute("data-anim"));
      }
    }
  }

  function setMarquees(safe) {
    /* A stopped marquee can freeze with its text scrolled out of view, so
       Safe Mode hides it and shows the same content as a static block. */
    var items = doc.getElementsByTagName("marquee");
    for (var i = 0; i < items.length; i++) {
      var m = items[i];
      var still = m.hsStatic;
      if (safe) {
        try { m.stop(); } catch (e) { /* stop() missing; hiding is enough */ }
        if (!still) {
          still = doc.createElement("div");
          still.className = "hs-marquee-static";
          still.innerHTML = m.innerHTML;
          m.parentNode.insertBefore(still, m.nextSibling);
          m.hsStatic = still;
        }
        still.style.display = "";
        m.style.display = "none";
      } else {
        if (still) { still.style.display = "none"; }
        m.style.display = "";
        try { m.start(); } catch (e) { /* start() missing; marquee keeps its default behavior */ }
      }
    }
  }

  function apply(safe, quiet) {
    if (safe) {
      if (!isSafe()) { root.className = (root.className + " hs-safe").replace(/^\s+/, ""); }
    } else {
      root.className = root.className.replace(/\s*\bhs-safe\b/g, "");
    }
    swapImages(safe);
    setMarquees(safe);
    if (safe) { stopAllAudio(); }
    if (toggle) {
      setPressed(toggle, safe);
      toggle.textContent = safe ? "SAFE MODE: ON" : "SAFE MODE: OFF";
    }
    window.HOMESTEAD_SAFE = safe;
    if (!quiet) {
      announce(safe ? "Safe Mode on. Motion and sound stopped, contrast raised." : "Safe Mode off.");
    }
  }

  function wireAudio() {
    var items = doc.querySelectorAll("[data-hs-audio]");
    for (var i = 0; i < items.length; i++) {
      (function (el) {
        var audio = new Audio();
        audio.preload = "none";
        audio.src = el.getAttribute("data-hs-audio");
        audio.loop = el.getAttribute("data-hs-loop") === "true";
        var player = { el: el, audio: audio };
        players.push(player);
        if (el.tagName !== "BUTTON") {
          el.setAttribute("role", "button");
          if (!el.hasAttribute("tabindex") && el.tagName !== "A") { el.setAttribute("tabindex", "0"); }
        }
        setPressed(el, false);
        audio.addEventListener("ended", function () { setPressed(el, false); });
        function activate(evt) {
          if (evt) { evt.preventDefault(); }
          if (isSafe()) {
            announce("Turn Safe Mode off to play music.");
            return;
          }
          if (audio.paused) {
            stopAllAudio();
            var started = audio.play();
            setPressed(el, true);
            announce("Music playing. Activate again to stop.");
            if (started && started["catch"]) {
              started["catch"](function () { setPressed(el, false); });
            }
          } else {
            audio.pause();
            audio.currentTime = 0;
            setPressed(el, false);
            announce("Music stopped.");
          }
        }
        el.addEventListener("click", activate);
        el.addEventListener("keydown", function (evt) {
          if (el.tagName !== "A" && (evt.key === "Enter" || evt.key === " ")) { activate(evt); }
        });
      })(items[i]);
    }
  }

  function build() {
    live = doc.createElement("div");
    live.className = "hs-visually-hidden";
    live.setAttribute("aria-live", "polite");
    doc.body.appendChild(live);

    toggle = doc.createElement("button");
    toggle.id = "hs-safe-toggle";
    toggle.type = "button";
    toggle.title = "Stops animation and sound and raises contrast";
    toggle.addEventListener("click", function () {
      var next = !isSafe();
      writeStored(next ? "on" : "off");
      apply(next, false);
    });
    doc.body.insertBefore(toggle, doc.body.firstChild);

    wireAudio();

    var stored = readStored();
    var start = stored === "on" ? true : stored === "off" ? false : prefersReducedMotion();
    apply(start, true);
    root.className = (root.className + " hs-ready").replace(/^\s+/, "");
  }

  window.homesteadSafe = isSafe;

  if (doc.readyState === "loading") {
    doc.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }
})();
