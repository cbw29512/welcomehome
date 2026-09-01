// Welcome Home — small progressive-enhancement script. No build step, no framework.
(function () {
  "use strict";

  // ---- Homepage species filter ----
  var tabs = document.querySelectorAll(".species-tabs button");
  if (tabs.length) {
    var rows = document.querySelectorAll(".checklist-row");
    var blocks = document.querySelectorAll(".category-block");

    function applyFilter(species) {
      rows.forEach(function (row) {
        var show = species === "all" || row.getAttribute("data-species") === species;
        row.style.display = show ? "" : "none";
      });
      blocks.forEach(function (block) {
        var visible = block.querySelectorAll('.checklist-row:not([style*="display: none"])').length;
        block.style.display = visible ? "" : "none";
      });
    }

    tabs.forEach(function (btn) {
      btn.addEventListener("click", function () {
        tabs.forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
        btn.setAttribute("aria-pressed", "true");
        applyFilter(btn.getAttribute("data-species"));
      });
    });
  }

  // ---- Worksheet checkbox persistence + pet name/date ----
  var worksheet = document.querySelector("[data-worksheet-id]");
  if (worksheet) {
    var id = worksheet.getAttribute("data-worksheet-id");
    var storeKey = "welcomehome:" + id;

    function loadState() {
      try {
        return JSON.parse(window.localStorage.getItem(storeKey) || "{}");
      } catch (e) {
        return {};
      }
    }
    function saveState(state) {
      try {
        window.localStorage.setItem(storeKey, JSON.stringify(state));
      } catch (e) { /* ignore */ }
    }

    var state = loadState();
    var boxes = worksheet.querySelectorAll('input[type="checkbox"]');
    var petName = worksheet.querySelector("#pet-name");
    var dateHome = worksheet.querySelector("#date-home");
    var progressEl = worksheet.querySelector("[data-progress]");

    function updateProgress() {
      if (!progressEl) return;
      var total = boxes.length;
      var done = 0;
      boxes.forEach(function (b) { if (b.checked) done++; });
      progressEl.textContent = done + " of " + total + " done";
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
        boxes.forEach(function (b) {
          b.checked = false;
          b.closest("li").classList.remove("checked");
        });
        if (petName) petName.value = "";
        if (dateHome) dateHome.value = "";
        updateProgress();
      });
    }

    updateProgress();
  }
})();
