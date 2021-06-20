// https://hant-kb.kaifa99.com/java/post_3636301
// https://cor.team/posts/Zh3r0%20CTF%20V2%20-%20All%20Pwnable%20Writeups#Javascript%20for%20Dummies%20Part%201
// hex to double 還不會用

JRS = function(){
    function numberToBinString(number, binStringLength) {
        var A = [], T = null; // number>=0
        while (binStringLength--) {
            T = number % 2;
            A[binStringLength] = T;
            number -= T;
            number /= 2;
        }
        return A.join("");
    }

    function HexFn(fourBitsBinString) {
        return parseInt(fourBitsBinString, 2).toString(16);
    }

    function binStringToHexString(binString) {
        return binString.replace(/(\d{4})/g, HexFn );
    }

    function hexStringToBinString(hexString) {
        var binString = "";

        for(var i=0; i< hexString.length-1; i+=2) {
            binString += numberToBinString(parseInt(hexString.substr(i, 2), 16), 8);
        }

        return binString;    
    }

    function SngFwd(Sg, Ex, Mt) {
        var B = {};
        Mt = Math.pow(2, 23) * Mt + 0.5; // round
        B.a = 0xFF & Mt;
        B.b = 0xFF & (Mt >> 8);
        B.c = 0x7F & (Mt >> 16) | (Ex & 1) << 7;
        B.d = Sg << 7 | (Ex >> 1);
        return B;
    }

    function DblFwd(Sg, Ex, Mt) {
        var B = {};
        Mt = Math.pow(2, 52) * Mt;
        B.a = 0xFFFF & Mt;
        B.b = 0xFFFF & (Mt >> 16);
        Mt /= Math.pow(2, 32); // Integers are only 32-bit
        B.c = 0xFFFF & Mt;
        B.d = Sg << 15 | Ex << 4 | 0x000F & (Mt >> 16);
        return B;
    }

    function CVTFWD(NumW, Qty) { // Function now without side-effects
        var Sign = null, Expo = null, Mant = null, Bin = null, nb01 = ""; // , OutW = NumW/4
        var Inf = {
            32 : {d: 0x7F, c: 0x80, b: 0, a : 0},
            64 : {d: 0x7FF0, c: 0, b: 0, a : 0}
        };
        var ExW = {32: 8, 64: 11}[NumW], MtW = NumW - ExW - 1;

        if (isNaN(Qty)) {
            Bin = Inf[NumW];
            Bin.a = 1;
            Sign = false;
            Expo = Math.pow(2, ExW) - 1;
            Mant = Math.pow(2, -MtW);
        }

        if (!Bin) {
            Sign = Qty < 0 || 1 / Qty < 0; // OK for +-0
            if (!isFinite(Qty)) {
                Bin = Inf[NumW];
                if (Sign)
                    Bin.d += 1 << (NumW / 4 - 1);
                Expo = Math.pow(2, ExW) - 1;
                Mant = 0;
            }
        }

        if (!Bin) {
            Expo = {32: 127, 64: 1023}[NumW];
            Mant = Math.abs(Qty);
            while (Mant >= 2) {
                Expo++;
                Mant /= 2;
            }
            while (Mant < 1 && Expo > 0) {
                Expo--;
                Mant *= 2;
            }
            if (Expo <= 0) {
                Mant /= 2;
                nb01 = "Zero or Denormal";
            }
            if (NumW == 32 && Expo > 254) {
                nb01 = "Too big for Single";
                Bin = {
                    d : Sign ? 0xFF : 0x7F,
                    c : 0x80,
                    b : 0,
                    a : 0
                };
                Expo = Math.pow(2, ExW) - 1;
                Mant = 0;
            }
        }

        if (!Bin)
            Bin = {32: SngFwd, 64: DblFwd}[NumW](Sign, Expo, Mant);

        Bin.sgn = +Sign;
        Bin.exp = numberToBinString(Expo, ExW);
        Mant = (Mant % 1) * Math.pow(2, MtW);
        if (NumW == 32)
            Mant = Math.floor(Mant + 0.5);
        Bin.mnt = numberToBinString(Mant, MtW);
        Bin.nb01 = nb01;
        return Bin;
    }

    function CVTREV(BinStr) {
        var ExW = {32: 8,64: 11}[BinStr.length];
        var M = BinStr.match(new RegExp("^(.)(.{" + ExW + "})(.*)$"));
        // M1 sign, M2 exponent, M3 mantissa

        var Sign = M[1] == "1" ? -1 : +1;

        if (!/0/.test(M[2])) { // NaN or Inf
            var X = /1/.test(M[3]) ? NaN : Sign / 0;
            throw new Error("Max Coded " + M[3] + " " + X.toString());
        }

        var Denorm = +M[2] == 0;
        if (Denorm) {
            console.log("Zero or Denormal");
        }

        var Expo = parseInt(M[2], 2) - Math.pow(2, ExW - 1) + 1;
        var Mant = parseInt(M[3], 2) / Math.pow(2, M[3].length) + !Denorm;
        return Sign * Mant * Math.pow(2, Expo + Denorm);
    }

    this.doubleToHexString = function( /* double */d, /* int */size) {
        var NumW = size;
        var Qty = d;
        with (CVTFWD(NumW, Qty)) {
            return binStringToHexString(sgn + exp + mnt);
        }
    };

    this.hexStringToDouble = function (/*String*/hexString, /*int*/size) {
        var NumW = size ;
        var binString = hexStringToBinString(hexString) ;
        console.log("binString = ", binString, binString.length);
        var X = new RegExp("^[01]{" + NumW + "}$");
        if (!X.test(binString)) {
            return;
        }
        return CVTREV(binString);
    };
};

jrs = new JRS()
HEX = parseInt(jrs.doubleToHexString(6.9244387627541e-310, 64), 16).toString(16)
HEX2 = jrs.doubleToHexString(6.9244387627541e-310, 64)

DOUBLE = jrs.hexStringToDouble(HEX2, 64)

console.log("HEX @ ", HEX)
console.log("DOUBLE @ ", DOUBLE)
