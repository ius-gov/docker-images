var fs = require('fs');

var args = process.argv.slice(2);


var fileName = args[0];
var stateCode = args[1];

var file = require(fileName);
console.log("Updating state code to ", stateCode);
file.state_code = stateCode;

fs.writeFile(fileName, JSON.stringify(file, null, 4), function (err) {
  if (err) 
    return console.log(err);
  console.log('writing to ' + fileName);
});