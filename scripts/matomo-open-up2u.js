 var _paq = window._paq || [];
  /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
  _paq.push(["setDocumentTitle", document.domain + "/" + document.title]);
  _paq.push(["setDomains", ["up2university.eu","*.sso.open.up2university.eu","*.cernbox.open.up2university.eu","*.learn.open.up2university.eu","*.meet01.open.up2university.eu","*.meet02.open.up2university.eu","*.meet03.open.up2university.eu","*.meet04.open.up2university.eu","*.meet05.open.up2university.eu","*.meet06.open.up2university.eu","*.swan.open.up2university.eu"]]);
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="//matomo.test.up2university.eu/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '7']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.type='text/javascript'; g.async=true; g.defer=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
  })();
