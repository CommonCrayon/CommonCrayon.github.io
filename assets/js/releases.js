// Fills download buttons and release details from GitHub Releases.
// Mark up a container with data-repo="Owner/Repo" and data-asset=".exe" (file extension to pick),
// then put data-download on the link and data-field="version|size|date|downloads|file" on text spots.
// If GitHub can't be reached, the links still point at the repo's latest release page.
(function () {
  const CACHE_MINUTES = 30;

  function cacheGet(key) {
    try {
      const raw = sessionStorage.getItem(key);
      if (!raw) return null;
      const { t, v } = JSON.parse(raw);
      return Date.now() - t < CACHE_MINUTES * 60000 ? v : null;
    } catch (e) { return null; }
  }
  function cacheSet(key, v) {
    try { sessionStorage.setItem(key, JSON.stringify({ t: Date.now(), v })); } catch (e) {}
  }

  function fmtSize(bytes) {
    if (!bytes) return "";
    const mb = bytes / 1048576;
    return mb >= 1 ? mb.toFixed(1) + " MB" : Math.round(bytes / 1024) + " KB";
  }
  function fmtDate(iso) {
    try {
      return new Date(iso).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" });
    } catch (e) { return ""; }
  }

  async function loadRepo(repo) {
    const key = "rel:" + repo;
    const cached = cacheGet(key);
    if (cached) return cached;
    const res = await fetch("https://api.github.com/repos/" + repo + "/releases?per_page=100", {
      headers: { Accept: "application/vnd.github+json" }
    });
    if (!res.ok) throw new Error("GitHub returned " + res.status);
    const all = await res.json();
    const slim = all.filter(r => !r.draft).map(r => ({
      tag: r.tag_name, name: r.name, pre: r.prerelease, date: r.published_at, url: r.html_url,
      assets: r.assets.map(a => ({ name: a.name, size: a.size, url: a.browser_download_url, count: a.download_count }))
    }));
    cacheSet(key, slim);
    return slim;
  }

  function fill(el, releases) {
    const ext = (el.dataset.asset || "").toLowerCase();
    const latest = releases.find(r => !r.pre) || releases[0];
    if (!latest) return;
    const asset = latest.assets.find(a => a.name.toLowerCase().endsWith(ext)) || latest.assets[0];
    const total = releases.reduce((n, r) => n + r.assets.reduce((m, a) => m + a.count, 0), 0);
    const version = latest.tag.replace(/^v/i, "").replace(/_/g, ".");

    const values = {
      version: "v" + version,
      file: asset ? asset.name : "",
      size: asset ? fmtSize(asset.size) : "",
      date: fmtDate(latest.date),
      downloads: total.toLocaleString()
    };
    el.querySelectorAll("[data-field]").forEach(n => {
      const v = values[n.dataset.field];
      if (v) { n.textContent = v; n.closest("[data-hide-empty]")?.removeAttribute("hidden"); }
    });
    el.querySelectorAll("[data-download]").forEach(a => {
      a.href = asset ? asset.url : latest.url;
      const label = a.querySelector("[data-label]");
      if (label) label.textContent = "Download v" + version;
    });
  }

  document.querySelectorAll("[data-repo]").forEach(async el => {
    try { fill(el, await loadRepo(el.dataset.repo)); }
    catch (e) { /* keep the fallback link to the releases page */ }
  });
})();
