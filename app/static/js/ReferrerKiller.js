var ReferrerKiller = (function() {
  var URL_REDIRECTION = "https://www.google.com/url?q=",
    PUB = {},
    IE_GT_8 = (function() {
      var trident,
        match = navigator.userAgent.match(/Trident\/(\d)+/);
      if (null === match) {
        return false;
      }
      trident = parseInt(match[1], 10);
      if (isNaN(trident)) {
        return false;
      }
      return trident > 4;
    })();

  function escapeDoubleQuotes(str) {
    return str.split('"').join('\\"');
  }

  function htmlToNode(html) {
    var container = document.createElement('div');
    container.innerHTML = html;
    return container.firstChild;
  }

  function objectToHtmlAttributes(obj) {
    var attributes = [],
      value;
    for (var name in obj) {
      value = obj[name];
      attributes.push(name + '="' + escapeDoubleQuotes(value) + '"');
    }
    return attributes.join(' ');
  }

  function htmlString(html, iframeAttributes) {
    var iframeAttributes = iframeAttributes || {},
      defaultStyles = 'border:none; overflow:hidden;',
      id;
    if (window.innerWidth < 768) {
      var width = window.innerWidth * 0.31;
    } else {
      var width = window.innerWidth * 0.16;
    }
    if ('style' in iframeAttributes) {
      iframeAttributes.style = defaultStyles + iframeAttributes.style;
    } else {
      iframeAttributes.style = defaultStyles;
    }
    id = '__referrer_killer_' + (new Date).getTime() + Math.floor(Math.random() * 9999);
    return '<iframe \
        marginwidth="0"\
        marginheight="0"\
        scrolling="no" \
        frameborder="no" \
        allowtransparency="true" ' +
      objectToHtmlAttributes(iframeAttributes) +
      'id="' + id + '" ' +
      '  src="javascript:\'\
      <!doctype html>\
      <html>\
      <head>\
      <meta charset=\\\'utf-8\\\'>\
      <style>*{margin:0;padding:0;border:0;}\
      .page-list-cover {\
        position: relative;\
        overflow: hidden;\
        background: #fff;\
        padding-top: 146.6666666%;\
        width: ' + width + 'px;\
        height: ' + width * 1.47 + 'px;\
        display: block;\
      }\
      .music-cover {\
        padding-top: 100%;\
      }\
      </style>\
      </head>' +
      '<script>\
         function resizeWindow() {\
          var elems  = document.getElementsByTagName(\\\'*\\\'),\
            width  = 0,\
            height = 0,\
            first  = document.body.firstChild,\
            elem;\
          if (first.offsetHeight && first.offsetWidth) {\
            width = first.offsetWidth;\
            height = first.offsetHeight;\
          } else {\
            for (var i in elems) {\
                      elem = elems[i];\
                      if (!elem.offsetWidth) {\
                        continue;\
                      }\
                      width  = Math.max(elem.offsetWidth, width);\
                      height = Math.max(elem.offsetHeight, height);\
            }\
          }\
          var ifr = parent.document.getElementById(\\\'' + id + '\\\');\
          ifr.height = height;\
          ifr.width  = width;\
        }\
      </script>' +
      '<body onload=\\\'resizeWindow()\\\'>\' + decodeURIComponent(\'' +
      encodeURIComponent(html) +
      '\') +\'</body></html>\'"></iframe>';
  }

  var linkHtml = PUB.linkHtml = function(url, innerHTML, anchorParams, iframeAttributes) {
    var html,
      urlRedirection = '';
    innerHTML = innerHTML || false;
    if (!innerHTML) {
      innerHTML = url;
    }
    anchorParams = anchorParams || {};
    if (!('target' in anchorParams) || '_self' === anchorParams.target) {
      anchorParams.target = '_top';
    }
    if (IE_GT_8) {
      urlRedirection = URL_REDIRECTION;
    }
    html = '<a rel="noreferrer" href="' + urlRedirection + escapeDoubleQuotes(url) + '" ' + objectToHtmlAttributes(anchorParams) + '>' + innerHTML + '</a>';
    return htmlString(html, iframeAttributes);
  };

  var linkNode = PUB.linkNode = function(url, innerHTML, anchorParams, iframeAttributes) {
    return htmlToNode(linkHtml(url, innerHTML, anchorParams, iframeAttributes));
  };

  var imageHtml = PUB.imageHtml = function(url, imgAttributesParam) {
    var imgAttributes = imgAttributesParam || {},
      defaultStyles = 'border:none; margin: 0; padding: 0;';
    if ('style' in imgAttributes) {
      imgAttributes.style = defaultStyles + imgAttributes.style;
    } else {
      imgAttributes.style = defaultStyles;
    }
    return htmlString('<img src="' + escapeDoubleQuotes(url) + '" ' + objectToHtmlAttributes(imgAttributes) + '/>');
  };

  var imageNode = PUB.imageNode = function(url, imgParams) {
    return htmlToNode(imageHtml(url, imgParams));
  };

  return PUB;
})();
