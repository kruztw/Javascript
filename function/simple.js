// standard
function f1() { return 1; }

console.log(f1());


// function pointer
f2 = function() { return 2; }

console.log(f2());


console.log( (function() { return 3; }()) );
