var window = {
//  TKK: parseInt(new Date().getTime() / 1000 / 60 / 60)
    TKK: "406416.489912402"
};

var sM = function(a) {
  return function() {
    return a
  }
}

var t  = "a";
var jd = ".";
var $b = "+-a^+6";
var Yb = "+";
var Zb = "+-3^+b+-f";
var cb = "&"
var k  = ""
var Gf = "="
var uM = null;

var tM = function(a, b) {
    for (var c = 0; c < b.length - 2; c += 3) {
        var d = b.charAt(c + 2)
          , d = d >= t ? d.charCodeAt(0) - 87 : Number(d)
          , d = b.charAt(c + 1) == Yb ? a >>> d : a << d;
        a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
    }
    return a
}

var vM = function(a) {
    var b;
    if (null  !== uM)
        b = uM;
    else {
        b = sM(String.fromCharCode(84));
        var c = sM(String.fromCharCode(75));
        b = [b(), b()];
        b[1] = c();
        b = (uM = window[b.join(c())] || k) || k
    }
    var d = sM(String.fromCharCode(116))
      , c = sM(String.fromCharCode(107))
      , d = [d(), d()];
    d[1] = c();
    c = cb + d.join(k) + Gf;
    d = b.split(jd);
    b = Number(d[0]) || 0;
    for (var e = [], f = 0, g = 0; g < a.length; g++) {
        var m = a.charCodeAt(g);
        128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
        e[f++] = m >> 18 | 240,
        e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
        e[f++] = m >> 6 & 63 | 128),
        e[f++] = m & 63 | 128)
    }
    a = b;
    for (f = 0; f < e.length; f++)
        a += e[f],
        a = tM(a, $b);
    a = tM(a, Zb);
    a ^= Number(d[1]) || 0;
    0 > a && (a = (a & 2147483647) + 2147483648);
    a %= 1E6;
    return (a.toString() + jd + (a ^ b))
}
