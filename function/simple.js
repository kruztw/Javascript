// standard
function f1() { return 1; }

console.log(f1());


// function pointer
f2 = function() { return 2; }

console.log(f2());


console.log( (function(a, b) { console.log("a+b =", a+b); return a+b; }(1, 2), function(){ return "callback"; }()) );


// return the last value
function f3() { return 1, 2; }

console.log(f3()); // 2
