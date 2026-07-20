/* Typeahead search over states, cities, communities, and operators.
   Index is lazy-loaded on first focus; everything runs client-side. */
(function () {
  if (window.__fsearchInit) return;
  window.__fsearchInit = true;

  var index = null, loading = null;
  var TYPE_LABEL = { state: "State", city: "City", facility: "Community", org: "Operator" };
  var TYPE_ORDER = { state: 0, city: 1, facility: 2, org: 3 };

  function norm(s) {
    return s.toLowerCase().replace(/[’']/g, "").replace(/[".,()–—-]/g, " ").replace(/\s+/g, " ").trim();
  }

  function loadIndex() {
    if (!loading) {
      loading = fetch("/assets/search-index.json")
        .then(function (r) { return r.json(); })
        .then(function (data) {
          index = data.filter(function (e) { return e.t !== "x"; });
          index.forEach(function (e) { e.h = norm(e.n + " " + (e.d || "")); e.nn = norm(e.n); });
        })
        .catch(function () { index = []; });
    }
    return loading;
  }

  function score(entry, tokens, q) {
    var name = entry.nn;
    for (var i = 0; i < tokens.length; i++) {
      if (entry.h.indexOf(tokens[i]) === -1) return -1;
    }
    if (name === q) return 0;
    if (name.indexOf(q) === 0) return 1;
    if (name.indexOf(" " + tokens[0]) !== -1 || name.indexOf(tokens[0]) === 0) return 2;
    return 3;
  }

  function search(q) {
    q = norm(q);
    if (!q || !index) return [];
    var tokens = q.split(/\s+/);
    var out = [];
    for (var i = 0; i < index.length; i++) {
      var s = score(index[i], tokens, q);
      if (s >= 0) out.push({ e: index[i], s: s });
    }
    out.sort(function (a, b) {
      return (a.s - b.s) || (TYPE_ORDER[a.e.t] - TYPE_ORDER[b.e.t]) || a.e.n.localeCompare(b.e.n);
    });
    return out.slice(0, 8).map(function (r) { return r.e; });
  }

  function setup(box) {
    var input = box.querySelector("input[type=search]");
    var list = box.querySelector(".fsearch-results");
    var form = box.querySelector("form");
    if (!input || !list) return;
    var results = [], active = -1;

    function close() { list.hidden = true; list.innerHTML = ""; active = -1; input.setAttribute("aria-expanded", "false"); }

    function render() {
      list.innerHTML = "";
      active = -1;
      if (!results.length) {
        if (input.value.trim().length >= 2) {
          var li = document.createElement("li");
          li.className = "fsearch-empty";
          li.innerHTML = 'No matches yet — <a href="/directory/">browse the directory</a>';
          list.appendChild(li);
          list.hidden = false;
        } else { close(); }
        return;
      }
      results.forEach(function (e, i) {
        var li = document.createElement("li");
        li.setAttribute("role", "option");
        li.id = input.id + "-opt-" + i;
        var a = document.createElement("a");
        a.href = e.u;
        a.innerHTML = "<strong></strong> <span class='fsearch-ctx'></span><span class='fsearch-type'></span>";
        a.querySelector("strong").textContent = e.n;
        a.querySelector(".fsearch-ctx").textContent = e.d || "";
        a.querySelector(".fsearch-type").textContent = TYPE_LABEL[e.t] || "";
        li.appendChild(a);
        li.addEventListener("mousedown", function (ev) { ev.preventDefault(); window.location.href = e.u; });
        list.appendChild(li);
      });
      list.hidden = false;
      input.setAttribute("aria-expanded", "true");
    }

    function highlight(n) {
      var opts = list.querySelectorAll("[role=option]");
      if (!opts.length) return;
      active = (n + opts.length) % opts.length;
      opts.forEach(function (o, i) { o.classList.toggle("active", i === active); });
      input.setAttribute("aria-activedescendant", opts[active].id);
    }

    input.addEventListener("focus", function () { loadIndex(); });
    input.addEventListener("input", function () {
      loadIndex().then(function () { results = search(input.value); render(); });
    });
    input.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowDown") { ev.preventDefault(); highlight(active + 1); }
      else if (ev.key === "ArrowUp") { ev.preventDefault(); highlight(active - 1); }
      else if (ev.key === "Escape") { close(); }
      else if (ev.key === "Enter") {
        if (active >= 0 && results[active]) { ev.preventDefault(); window.location.href = results[active].u; }
        else if (results.length) { ev.preventDefault(); window.location.href = results[0].u; }
      }
    });
    input.addEventListener("blur", function () { setTimeout(close, 150); });
    if (form) form.addEventListener("submit", function (ev) {
      if (results.length) { ev.preventDefault(); window.location.href = results[0].u; }
    });
  }

  function init() { document.querySelectorAll(".fsearch").forEach(setup); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
