// Lazy AdSense loader: nothing ad-related is fetched until an ad slot is
// about to scroll into view. Keeps first paint and LCP clean.
(function () {
  var slots = document.querySelectorAll('.ad-slot[data-ad-slot]');
  if (!slots.length || !('IntersectionObserver' in window)) return;
  var pub = document.documentElement.getAttribute('data-adsense-pub');
  if (!pub) return;
  var loaded = false;
  function loadAdsense() {
    if (loaded) return;
    loaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.crossOrigin = 'anonymous';
    s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + pub;
    document.head.appendChild(s);
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      loadAdsense();
      var ins = document.createElement('ins');
      ins.className = 'adsbygoogle';
      ins.style.display = 'block';
      ins.setAttribute('data-ad-client', pub);
      ins.setAttribute('data-ad-format', 'auto');
      ins.setAttribute('data-full-width-responsive', 'true');
      if (e.target.dataset.adSlot !== 'auto') ins.setAttribute('data-ad-slot', e.target.dataset.adSlot);
      e.target.textContent = '';
      e.target.appendChild(ins);
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    });
  }, { rootMargin: '600px 0px' });
  slots.forEach(function (s) { io.observe(s); });
})();
