function myFunc(x, y, ...params) { // used rest operator here
  console.log(x);
  console.log(y);
  console.log(params);
}

var inputs = ["a", "b", "c", "d", "e", "f"];
myFunc(...inputs);


function myFunc2(...[x, y, z]) {
  console.log(x);
  console.log(y);
  console.log(z);
}

myFunc2(1)      
myFunc2(1, 2, 3)    
myFunc2(1, 2, 3, 4) // 沒用到第四個參數 
