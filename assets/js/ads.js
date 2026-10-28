// Google AdSense setup. These two values are the only things to change.
// 1. ADSENSE_CLIENT: your publisher ID from AdSense (Account > Account information), e.g. "ca-pub-1234567890123456".
// 2. ADSENSE_SLOT: the ID of a display ad unit (Ads > By ad unit > Display ads), e.g. "1234567890".
// Also put the same publisher ID in /ads.txt.
const ADSENSE_CLIENT = "";
const ADSENSE_SLOT = "";

(function () {
  const slots = document.querySelectorAll(".ad-slot");
  if (!slots.length) return;

  if (!ADSENSE_CLIENT || !ADSENSE_SLOT) {
    // Not set up yet: show a placeholder box when previewing locally, and hide the slots on the live site.
    const local = location.protocol === "file:" || /^(localhost|127\.0\.0\.1)$/.test(location.hostname);
    slots.forEach(s => {
      if (local) { s.classList.add("is-preview"); s.textContent = "Ad space. Add your AdSense IDs in assets/js/ads.js"; }
      else { s.hidden = true; }
    });
    return;
  }

  const script = document.createElement("script");
  script.async = true;
  script.crossOrigin = "anonymous";
  script.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" + ADSENSE_CLIENT;
  document.head.appendChild(script);

  window.adsbygoogle = window.adsbygoogle || [];
  slots.forEach(s => {
    const ins = document.createElement("ins");
    ins.className = "adsbygoogle";
    ins.style.display = "block";
    ins.setAttribute("data-ad-client", ADSENSE_CLIENT);
    ins.setAttribute("data-ad-slot", ADSENSE_SLOT);
    ins.setAttribute("data-ad-format", "auto");
    ins.setAttribute("data-full-width-responsive", "true");
    s.appendChild(ins);
    window.adsbygoogle.push({});
  });
})();
