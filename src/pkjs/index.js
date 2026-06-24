// Farsi Fuzzy Watchface - Companion App Settings
Pebble.addEventListener('showConfiguration', function() {
  var config = { AccuracyLevel: 0, ThemeColor: 0 };
  var saved = localStorage.getItem('farsi_config');
  if (saved) {
    try { config = JSON.parse(saved); } catch(e){}
  }

  var url = 'data:text/html,' + encodeURIComponent(
    '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">' +
    '<style>' +
    'body{font-family:-apple-system,sans-serif;background:#1a1a2e;color:#fff;margin:0;padding:20px;direction:rtl}' +
    'h1{text-align:center;color:#e94560;font-size:22px;margin-bottom:5px}' +
    'h2{text-align:center;color:#888;font-size:14px;margin-top:0}' +
    '.option{background:#16213e;border:2px solid #0f3460;border-radius:12px;padding:15px;margin:10px 0;cursor:pointer;transition:all 0.2s}' +
    '.option:active,.option.selected{border-color:#e94560;background:#0f3460}' +
    '.option h3{margin:0 0 5px;font-size:16px;color:#e94560}' +
    '.option p{margin:0;font-size:13px;color:#aaa}' +
    '.option .example{font-size:18px;color:#fff;margin-top:8px;font-weight:bold}' +
    '.theme-toggle{background:#16213e;border:2px solid #0f3460;border-radius:12px;padding:15px;margin:20px 0;display:flex;justify-content:space-between;align-items:center;}' +
    '.switch{position:relative;display:inline-block;width:60px;height:34px;}' +
    '.switch input{opacity:0;width:0;height:0;}' +
    '.slider{position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background-color:#0f3460;transition:.4s;border-radius:34px;}' +
    '.slider:before{position:absolute;content:"";height:26px;width:26px;left:4px;bottom:4px;background-color:white;transition:.4s;border-radius:50%;}' +
    'input:checked+.slider{background-color:#e94560;}' +
    'input:checked+.slider:before{transform:translateX(26px);}' +
    'button{display:block;width:100%;padding:15px;background:#e94560;color:#fff;border:none;border-radius:12px;font-size:18px;margin-top:20px;cursor:pointer}' +
    '</style></head><body>' +
    '<h1>ساعت فازی فارسی</h1>' +
    '<h2>Farsi Fuzzy Time</h2>' +
    '<div class="theme-toggle">' +
    '<div><h3>تم روشن</h3><p style="margin:0;font-size:13px;color:#aaa">متن مشکی در پس‌زمینه سفید</p></div>' +
    '<label class="switch"><input type="checkbox" id="themeCheck" ' + (config.ThemeColor ? 'checked' : '') + '><span class="slider"></span></label>' +
    '</div>' +
    '<div id="options"></div>' +
    '<button onclick="save()">ذخیره</button>' +
    '<script>' +
    'var sel=' + config.AccuracyLevel + ';' +
    'var opts=[' +
    '{t:"ربع ساعت",d:"دقت ۱۵ دقیقه",ex:"ساعت یازده و ربع ا"},' +
    '{t:"نیم ساعت",d:"دقت ۳۰ دقیقه",ex:"ساعت یازده و نیم ا"},' +
    '{t:"ساعت",d:"دقت یک ساعت",ex:"ساعت یازده ا"},' +
    '{t:"نیم‌روز",d:"صبح یا شب",ex:"صبحه"},' +
    '{t:"روز و شب",d:"روز یا شب",ex:"روزه"},' +
    '{t:"بخش‌های روز",d:"۵ بخش",ex:"ظهره"}' +
    '];' +
    'var c=document.getElementById("options");' +
    'opts.forEach(function(o,i){' +
    'var d=document.createElement("div");d.className="option"+(i===sel?" selected":"");' +
    'd.innerHTML="<h3>"+o.t+"</h3><p>"+o.d+"</p><div class=example>"+o.ex+"</div>";' +
    'd.onclick=function(){sel=i;document.querySelectorAll(".option").forEach(function(e){e.className="option"});d.className="option selected"};' +
    'c.appendChild(d)});' +
    'function save(){' +
    'var isLight=document.getElementById("themeCheck").checked?1:0;' +
    'var r=JSON.stringify({AccuracyLevel:sel,ThemeColor:isLight});' +
    'window.location.href="pebblejs://close#"+encodeURIComponent(r)}' +
    '</script></body></html>'
  );
  Pebble.openURL(url);
});

Pebble.addEventListener('webviewclosed', function(e) {
  if (e && e.response && e.response !== 'CANCELLED') {
    var config = JSON.parse(decodeURIComponent(e.response));
    localStorage.setItem('farsi_config', JSON.stringify(config));
    
    var dict = { 
        'AccuracyLevel': config.AccuracyLevel,
        'ThemeColor': config.ThemeColor
    };
    Pebble.sendAppMessage(dict, function() {
      console.log('Settings sent successfully');
    }, function() {
      console.log('Settings failed to send');
    });
  }
});
