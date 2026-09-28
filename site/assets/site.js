// Welcome Home — small progressive-enhancement script. No build step, no framework.
(function () {
  "use strict";

  function warn(message, error) {
    if (window.console && typeof window.console.warn === "function") {
      window.console.warn("Welcome Home: " + message, error || "");
    }
  }

  // ---- Print button (only shown when JavaScript can run window.print) ----
  var printBtn = document.querySelector("[data-print]");
  if (printBtn && typeof window.print === "function") {
    printBtn.hidden = false;
    printBtn.addEventListener("click", function () { window.print(); });
  }

  // ---- Worksheet checkbox persistence + pet name/date ----
  var worksheet = document.querySelector("[data-worksheet-id]");
  if (worksheet) {
    var id = worksheet.getAttribute("data-worksheet-id");
    var storeKey = "welcomehome:" + id;

    function loadState() {
      try {
        return JSON.parse(window.localStorage.getItem(storeKey) || "{}");
      } catch (error) {
        warn("could not read saved worksheet state", error);
        return {};
      }
    }

    function saveState(state) {
      try {
        window.localStorage.setItem(storeKey, JSON.stringify(state));
      } catch (error) {
        warn("could not save worksheet state", error);
      }
    }

    var state = loadState();
    var boxes = worksheet.querySelectorAll('input[type="checkbox"]');
    // Pet name/date inputs live in the worksheet header, outside [data-worksheet-id].
    var petName = document.querySelector("#pet-name");
    var dateHome = document.querySelector("#date-home");
    var progressEl = worksheet.querySelector("[data-progress]");
    var progressBar = worksheet.querySelector("[data-progress-bar]");
    var SUPPORT_URL = "https://buymeacoffee.com/divclass016";

    function supportLink(className, text) {
      var link = document.createElement("a");
      link.className = className;
      link.href = SUPPORT_URL;
      link.target = "_blank";
      link.rel = "noopener";
      link.textContent = text;
      return link;
    }

    // The support card and header link are rendered in the HTML (generate_site.py).

    // Gentle thank-you once every item is checked off.
    var doneNote = document.createElement("p");
    doneNote.className = "progress-note";
    doneNote.hidden = true;
    doneNote.appendChild(document.createTextNode("All done \u2014 welcome home! If this checklist helped, "));
    doneNote.appendChild(supportLink("", "you can buy me a coffee"));
    doneNote.appendChild(document.createTextNode(" to keep Welcome Home free."));
    doneNote.className = "progress-note done-note";
    var progressBox = progressEl && (progressEl.closest(".progress-box") || progressEl.closest(".progress-note"));
    if (progressBox && progressBox.parentNode) progressBox.parentNode.insertBefore(doneNote, progressBox.nextSibling);

    function updateProgress() {
      if (!progressEl) return;
      var total = boxes.length;
      var done = 0;
      boxes.forEach(function (box) { if (box.checked) done += 1; });
      progressEl.textContent = done + " of " + total + " done";
      if (progressBar) progressBar.style.width = (total ? Math.round((done / total) * 100) : 0) + "%";
      doneNote.hidden = !(total > 0 && done === total);
    }

    boxes.forEach(function (box) {
      var key = box.id;
      if (state.checks && state.checks[key]) {
        box.checked = true;
        box.closest("li").classList.add("checked");
      }
      box.addEventListener("change", function () {
        state.checks = state.checks || {};
        state.checks[key] = box.checked;
        box.closest("li").classList.toggle("checked", box.checked);
        saveState(state);
        updateProgress();
      });
    });

    if (petName) {
      petName.value = state.petName || "";
      petName.addEventListener("input", function () {
        state.petName = petName.value;
        saveState(state);
      });
    }
    if (dateHome) {
      dateHome.value = state.dateHome || "";
      dateHome.addEventListener("input", function () {
        state.dateHome = dateHome.value;
        saveState(state);
      });
    }

    var resetBtn = worksheet.querySelector("[data-reset]");
    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        if (!window.confirm("Clear all checked items on this worksheet?")) return;
        state = {};
        saveState(state);
        boxes.forEach(function (box) {
          box.checked = false;
          box.closest("li").classList.remove("checked");
        });
        if (petName) petName.value = "";
        if (dateHome) dateHome.value = "";
        updateProgress();
      });
    }

    updateProgress();
  }
})();
