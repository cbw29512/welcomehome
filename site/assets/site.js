// Welcome Home — small progressive-enhancement script. No build step, no framework.
(function () {
  "use strict";

  function warn(message, error) {
    if (window.console && typeof window.console.warn === "function") {
      window.console.warn("Welcome Home: " + message, error || "");
    }
  }

  // ---- Homepage species filter ----
  var tabs = document.querySelectorAll(".species-tabs button");
  if (tabs.length) {
    var rows = document.querySelectorAll(".checklist-row");
    var blocks = document.querySelectorAll(".category-block");

    function applyFilter(species) {
      rows.forEach(function (row) {
        row.hidden = !(species === "all" || row.getAttribute("data-species") === species);
      });
      blocks.forEach(function (block) {
        var blockRows = block.querySelectorAll(".checklist-row");
        var visible = false;
        blockRows.forEach(function (row) {
          if (!row.hidden) visible = true;
        });
        block.hidden = !visible;
      });
    }

    tabs.forEach(function (btn) {
      btn.addEventListener("click", function () {
        tabs.forEach(function (button) { button.setAttribute("aria-pressed", "false"); });
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
    var petName = worksheet.querySelector("#pet-name");
    var dateHome = worksheet.querySelector("#date-home");
    var progressEl = worksheet.querySelector("[data-progress]");

    function updateProgress() {
      if (!progressEl) return;
      var total = boxes.length;
      var done = 0;
      boxes.forEach(function (box) { if (box.checked) done += 1; });
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
