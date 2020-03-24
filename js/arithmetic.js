'use strict';
const { PerformanceObserver, performance } = require('perf_hooks');
var fs = require("fs");
const assert = require('assert');
const binding = require.resolve(`../build/Release/binding`);
const maincpp = require(binding);
//const postfix = require('./postfix.js');


console.log(maincpp.addwrong("3123","691","3714"));
console.log(maincpp.subtractwrong("612","498","224") );