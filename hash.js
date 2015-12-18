// TKK = hours since epoch
var window = {
  TKK: parseInt(new Date().getTime() / 1000 / 60 / 60)
};

var t  = "a";
var cb = "&";
var mf = "=";
var k  = "";
var dd = ".";
var Vb = "+-a^+6";
var Tb = "+";
var Ub = "+-3^+b+-f";
var SL = null;

var QL = function(a) {
  return function() {
      return a;
  }
}

var RL = function(a, b) {
  for (var c = 0; c < b.length - 2; c += 3) {
      var d = b.charAt(c + 2)
        , d = d >= t ? d.charCodeAt(0) - 87 : Number(d)
        , d = b.charAt(c + 1) == Tb ? a >>> d : a << d;
      a = b.charAt(c) == Tb ? a + d & 4294967295 : a ^ d
  }
  return a;
}

var TL = function(a) {
    var b;
    if (null  === SL) {
        var c = QL(String.fromCharCode(84));
        b = QL(String.fromCharCode(75));
        c = [c(), c()];
        c[1] = b();
        SL = Number(window[c.join(b())]) || 0
    }
    b = SL;
    var d = QL(String.fromCharCode(116))
      , c = QL(String.fromCharCode(107))
      , d = [d(), d()];
    d[1] = c();
    for (var c = cb + d.join(k) + mf, d = [], e = 0, f = 0; f < a.length; f++) {
        var g = a.charCodeAt(f);
        128 > g ? d[e++] = g : (2048 > g ? d[e++] = g >> 6 | 192 : (55296 == (g & 64512) && f + 1 < a.length && 56320 == (a.charCodeAt(f + 1) & 64512) ? (g = 65536 + ((g & 1023) << 10) + (a.charCodeAt(++f) & 1023),
        d[e++] = g >> 18 | 240,
        d[e++] = g >> 12 & 63 | 128) : d[e++] = g >> 12 | 224,
        d[e++] = g >> 6 & 63 | 128),
        d[e++] = g & 63 | 128)
    }
    a = b || 0;
    for (e = 0; e < d.length; e++)
        a += d[e],
        a = RL(a, Vb);
    a = RL(a, Ub);
    0 > a && (a = (a & 2147483647) + 2147483648);
    a %= 1E6;
    return a.toString() + dd + (a ^ b)
}
