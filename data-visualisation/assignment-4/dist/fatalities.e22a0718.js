// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles
parcelRequire = (function (modules, cache, entry, globalName) {
  // Save the require from previous bundle to this closure if any
  var previousRequire = typeof parcelRequire === 'function' && parcelRequire;
  var nodeRequire = typeof require === 'function' && require;

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire = typeof parcelRequire === 'function' && parcelRequire;
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error('Cannot find module \'' + name + '\'');
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;
      localRequire.cache = {};

      var module = cache[name] = new newRequire.Module(name);

      modules[name][0].call(module.exports, localRequire, module, module.exports, this);
    }

    return cache[name].exports;

    function localRequire(x){
      return newRequire(localRequire.resolve(x));
    }

    function resolve(x){
      return modules[name][1][x] || x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;
  newRequire.register = function (id, exports) {
    modules[id] = [function (require, module) {
      module.exports = exports;
    }, {}];
  };

  var error;
  for (var i = 0; i < entry.length; i++) {
    try {
      newRequire(entry[i]);
    } catch (e) {
      // Save first error but execute all entries
      if (!error) {
        error = e;
      }
    }
  }

  if (entry.length) {
    // Expose entry point to Node, AMD or browser globals
    // Based on https://github.com/ForbesLindesay/umd/blob/master/template.js
    var mainExports = newRequire(entry[entry.length - 1]);

    // CommonJS
    if (typeof exports === "object" && typeof module !== "undefined") {
      module.exports = mainExports;

    // RequireJS
    } else if (typeof define === "function" && define.amd) {
     define(function () {
       return mainExports;
     });

    // <script>
    } else if (globalName) {
      this[globalName] = mainExports;
    }
  }

  // Override the current require with this new one
  parcelRequire = newRequire;

  if (error) {
    // throw error from earlier, _after updating parcelRequire_
    throw error;
  }

  return newRequire;
})({"static/js/fatalities.js":[function(require,module,exports) {
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.on_data = on_data;
function _typeof(o) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, _typeof(o); }
function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }
function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }
function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter); }
function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }
function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }
function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }
function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) arr2[i] = arr[i]; return arr2; }
function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, _toPropertyKey(descriptor.key), descriptor); } }
function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }
function _toPropertyKey(t) { var i = _toPrimitive(t, "string"); return "symbol" == _typeof(i) ? i : String(i); }
function _toPrimitive(t, r) { if ("object" != _typeof(t) || !t) return t; var e = t[Symbol.toPrimitive]; if (void 0 !== e) { var i = e.call(t, r || "default"); if ("object" != _typeof(i)) return i; throw new TypeError("@@toPrimitive must return a primitive value."); } return ("string" === r ? String : Number)(t); }
function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }
var config = {
  test: true,
  scrubber: {
    height: 5,
    width: 300
  }
};
var ONE_DAY_MS = 24 * 60 * 60 * 1000;
var TimeInterval = /*#__PURE__*/_createClass(function TimeInterval(end, length) {
  _classCallCheck(this, TimeInterval);
  this.start = end - length;
  this.end = end;
  if (this.start > this.end) throw Error("can't have start after end");
  this.start_noon = get_noon_epoch_time(this.start);
  this.end_noon = get_noon_epoch_time(this.end);
  if (this.end_noon > this.end) {
    this.end_noon = this.end_noon - ONE_DAY_MS;
  }
  this.elapsed_noons = [];
  if (this.start <= this.start_noon && this.end >= this.start_noon) {
    this.elapsed_noons.push(this.start_noon);
  }
  var current_noon = this.start_noon + ONE_DAY_MS;
  while (current_noon <= this.end_noon) {
    this.elapsed_noons.push(current_noon);
    current_noon = current_noon + ONE_DAY_MS;
  }
});
function interval_to_data(data, interval) {
  var fatalities = [];
  var _iterator = _createForOfIteratorHelper(interval.elapsed_noons),
    _step;
  try {
    for (_iterator.s(); !(_step = _iterator.n()).done;) {
      var noon = _step.value;
      var new_noons = data.get(noon);
      if (new_noons instanceof Array) {
        fatalities.push.apply(fatalities, _toConsumableArray(new_noons));
      }
    }
  } catch (err) {
    _iterator.e(err);
  } finally {
    _iterator.f();
  }
  return fatalities;
}
function on_response(response) {
  if (!response.ok) {
    throw new Error("failed to fetch data");
  }
  return response.json();
}
function assert_non_null(item) {
  if (item === null) {
    throw new Error("found null item");
  }
  return item;
}
function parse_date(str) {
  return assert_non_null(d3.timeParse("%Y-%m-%d")(str));
}
function create_thresholds(startDate, endDate, days) {
  var thresholds = [startDate];
  var currentDate = new Date(startDate);
  while (currentDate <= endDate) {
    currentDate = new Date(currentDate.getTime() + days * 86400000); // Add 'days' days
    thresholds.push(currentDate);
  }
  return thresholds;
}
function days_to_ms(days) {
  return days * days_to_ms.factor;
}
days_to_ms.factor = 24 * 60 * 60 * 1000;
function ms_to_days(ms) {
  return ms / days_to_ms.factor;
}
function get_noon_epoch_time(milliseconds) {
  var date = new Date(milliseconds);
  date.setHours(12, 0, 0, 0);
  return date.getTime();
}
function yeet(error_msg) {
  throw new Error(error_msg);
}
var debug = {
  noon_times: function noon_times(noon_time_to_fatalities) {
    var _iterator2 = _createForOfIteratorHelper(noon_time_to_fatalities.keys()),
      _step2;
    try {
      for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
        var k = _step2.value;
        console.log(new Date(k));
      }
    } catch (err) {
      _iterator2.e(err);
    } finally {
      _iterator2.f();
    }
  }
};
function on_data(data) {
  d3.select("#vis").selectAll("*").remove();
  var width = window.innerWidth * 0.9;
  var height = Number(window.innerHeight) * 0.95;
  var margin = {
    top: 200,
    right: 20,
    bottom: 20,
    left: 20
  };
  var histogram_center = 300;
  var histogram_height = 100;
  var noon_time_to_fatalities = new Map();
  data.forEach(function (d) {
    d.parsed_date = parse_date(d.date_of_death);
    d.parsed_date.setHours(12, 0, 0, 0);
    d.parsed_date_ms = d.parsed_date.getTime();
    var fatalities_list = noon_time_to_fatalities.get(d.parsed_date_ms);
    if (fatalities_list) {
      fatalities_list.push(d);
    } else {
      noon_time_to_fatalities.set(d.parsed_date_ms, [d]);
    }
  });
  debug.noon_times(noon_time_to_fatalities);
  data.sort(function (a, b) {
    return a.parsed_date_ms - b.parsed_date_ms;
  });
  var israeli_deaths = data.filter(function (d) {
    return d.citizenship === "Israeli";
  });
  var palestinian_deaths = data.filter(function (d) {
    return d.citizenship === "Palestinian";
  });
  var svg = d3.select('#vis').append('svg').attr('width', width).attr('height', height).append("g").attr("transform", "translate(".concat(margin.left, ",").concat(margin.top, ")"));
  var scrubber = svg.append('rect').attr('x', 0).attr('y', histogram_center).attr('width', config.scrubber.width).attr('height', config.scrubber.height).attr('opacity', 0.3).attr('stroke', 'white  ');
  var dateRange = d3.extent(data, function (d) {
    return d.parsed_date;
  });
  var time_zero = dateRange[0].getTime();
  var totalMilliseconds = dateRange[1].getTime() - time_zero;
  var totalDays = ms_to_days(totalMilliseconds);
  var histogram_width = width - margin.left - margin.right;
  var pixelsPerDay = histogram_width / totalDays;
  var daysPerSecond = 31; // 365 * 5;
  var days_data_per_ms_real = daysPerSecond / 1000;
  var ms_data_per_ms_real = days_to_ms(days_data_per_ms_real);
  var animationDuration = totalDays / days_data_per_ms_real;
  var framesPerSecond = 60;
  var frames_per_ms = 1000 / framesPerSecond;
  var pixelsPerTick = pixelsPerDay * daysPerSecond / framesPerSecond;
  var x = d3.scaleTime().domain(dateRange).range([0, histogram_width]);
  var padding_time = widthToMilliseconds(config.scrubber.width);
  var scrub_x = d3.scaleTime().domain([time_zero - padding_time, dateRange[1].getTime()]).range([-config.scrubber.width, histogram_width]).clamp(false);
  var totalWidthMilliseconds = totalMilliseconds + padding_time;
  function widthToMilliseconds(widthInPixels) {
    var oneDayPixelValue = x(new Date(time_zero + days_to_ms(1)));
    var days = widthInPixels / oneDayPixelValue;
    return days * (1000 / days_data_per_ms_real);
  }
  function ms_change_real_to_ms_change_data(ms_real) {
    return ms_real * ms_data_per_ms_real;
  }
  var elapsed_last = 0;
  function histogram_tick(elapsed) {
    var elapsed_diff = elapsed - elapsed_last;
    var looped_epoch_time = elapsed * ms_data_per_ms_real % totalWidthMilliseconds;
    var current_time_right_ms = time_zero + looped_epoch_time;
    var current_time_left_ms = current_time_right_ms - padding_time;
    var scenario_elapsed = ms_change_real_to_ms_change_data(elapsed_diff);
    var new_data_interval = new TimeInterval(current_time_right_ms, scenario_elapsed);
    var new_data = interval_to_data(noon_time_to_fatalities, new_data_interval);
    //console.log(elapsed, scenario_elapsed, new_data_interval);
    if (new_data_interval.elapsed_noons.length > 0) {
      // console.log("Elapsed noons:", new_data, new_data_interval);
      // console.log(noon_time_to_fatalities[new_data_interval.elapsed_noons[0]])
    }
    var x_val = scrub_x(current_time_left_ms);
    var real_x = d3.max([0, x_val]) || 0;
    var subtraction_left = d3.min([x_val, 0]) || 0;
    var width = d3.min([config.scrubber.width, histogram_width - real_x]) + subtraction_left;
    scrubber.attr('x', real_x).attr('width', width);
    elapsed_last = elapsed;
  }
  d3.interval(histogram_tick, frames_per_ms);
  var xAxis = svg.append("g").attr("transform", "translate(0,".concat(margin.top, ")"));
  var thresholds = create_thresholds(dateRange[0], dateRange[1], 14);
  var histogram = d3.bin().value(function (d) {
    return d.parsed_date;
  }).domain(x.domain()).thresholds(thresholds);
  var israeli_bins = histogram(israeli_deaths);
  var palestinian_bins = histogram(palestinian_deaths);
  var y_range = height - margin.top - margin.bottom;
  var rect_height = d3.scaleLinear().range([histogram_height, 0])
  // use the max of both israeli and palestinian deaths so both are on the same scale
  .domain([d3.max(histogram(data), function (d) {
    return d.length;
  }), 0]);
  function bin_width(d) {
    return Math.max(0, x(d.x1) - x(d.x0));
  }
  svg.selectAll("rect").data(israeli_bins).enter().append("rect").attr("x", function (d) {
    return x(d.x0);
  }).attr("y", function (d) {
    return histogram_center + config.scrubber.height;
  }).attr("width", function (d) {
    return bin_width(d);
  }).attr("height", function (d) {
    return rect_height(d.length);
  }).style("fill", "#0038b8");
  svg.selectAll(".palestinian-rect").data(palestinian_bins).enter().append("rect").attr("class", "palestinian-rect").attr("x", function (d) {
    return x(d.x0);
  }).attr("y", function (d) {
    return histogram_center - rect_height(d.length);
  }).attr("width", function (d) {
    return bin_width(d);
  }).attr("height", function (d) {
    return rect_height(d.length);
  }).style("fill", "#EE2A35");
}
fetch('/static/json/fatalities.json').then(on_response).then(on_data);
},{}],"node_modules/parcel-bundler/src/builtins/hmr-runtime.js":[function(require,module,exports) {
var global = arguments[3];
var OVERLAY_ID = '__parcel__error__overlay__';
var OldModule = module.bundle.Module;
function Module(moduleName) {
  OldModule.call(this, moduleName);
  this.hot = {
    data: module.bundle.hotData,
    _acceptCallbacks: [],
    _disposeCallbacks: [],
    accept: function (fn) {
      this._acceptCallbacks.push(fn || function () {});
    },
    dispose: function (fn) {
      this._disposeCallbacks.push(fn);
    }
  };
  module.bundle.hotData = null;
}
module.bundle.Module = Module;
var checkedAssets, assetsToAccept;
var parent = module.bundle.parent;
if ((!parent || !parent.isParcelRequire) && typeof WebSocket !== 'undefined') {
  var hostname = "" || location.hostname;
  var protocol = location.protocol === 'https:' ? 'wss' : 'ws';
  var ws = new WebSocket(protocol + '://' + hostname + ':' + "39387" + '/');
  ws.onmessage = function (event) {
    checkedAssets = {};
    assetsToAccept = [];
    var data = JSON.parse(event.data);
    if (data.type === 'update') {
      var handled = false;
      data.assets.forEach(function (asset) {
        if (!asset.isNew) {
          var didAccept = hmrAcceptCheck(global.parcelRequire, asset.id);
          if (didAccept) {
            handled = true;
          }
        }
      });

      // Enable HMR for CSS by default.
      handled = handled || data.assets.every(function (asset) {
        return asset.type === 'css' && asset.generated.js;
      });
      if (handled) {
        console.clear();
        data.assets.forEach(function (asset) {
          hmrApply(global.parcelRequire, asset);
        });
        assetsToAccept.forEach(function (v) {
          hmrAcceptRun(v[0], v[1]);
        });
      } else if (location.reload) {
        // `location` global exists in a web worker context but lacks `.reload()` function.
        location.reload();
      }
    }
    if (data.type === 'reload') {
      ws.close();
      ws.onclose = function () {
        location.reload();
      };
    }
    if (data.type === 'error-resolved') {
      console.log('[parcel] ✨ Error resolved');
      removeErrorOverlay();
    }
    if (data.type === 'error') {
      console.error('[parcel] 🚨  ' + data.error.message + '\n' + data.error.stack);
      removeErrorOverlay();
      var overlay = createErrorOverlay(data);
      document.body.appendChild(overlay);
    }
  };
}
function removeErrorOverlay() {
  var overlay = document.getElementById(OVERLAY_ID);
  if (overlay) {
    overlay.remove();
  }
}
function createErrorOverlay(data) {
  var overlay = document.createElement('div');
  overlay.id = OVERLAY_ID;

  // html encode message and stack trace
  var message = document.createElement('div');
  var stackTrace = document.createElement('pre');
  message.innerText = data.error.message;
  stackTrace.innerText = data.error.stack;
  overlay.innerHTML = '<div style="background: black; font-size: 16px; color: white; position: fixed; height: 100%; width: 100%; top: 0px; left: 0px; padding: 30px; opacity: 0.85; font-family: Menlo, Consolas, monospace; z-index: 9999;">' + '<span style="background: red; padding: 2px 4px; border-radius: 2px;">ERROR</span>' + '<span style="top: 2px; margin-left: 5px; position: relative;">🚨</span>' + '<div style="font-size: 18px; font-weight: bold; margin-top: 20px;">' + message.innerHTML + '</div>' + '<pre>' + stackTrace.innerHTML + '</pre>' + '</div>';
  return overlay;
}
function getParents(bundle, id) {
  var modules = bundle.modules;
  if (!modules) {
    return [];
  }
  var parents = [];
  var k, d, dep;
  for (k in modules) {
    for (d in modules[k][1]) {
      dep = modules[k][1][d];
      if (dep === id || Array.isArray(dep) && dep[dep.length - 1] === id) {
        parents.push(k);
      }
    }
  }
  if (bundle.parent) {
    parents = parents.concat(getParents(bundle.parent, id));
  }
  return parents;
}
function hmrApply(bundle, asset) {
  var modules = bundle.modules;
  if (!modules) {
    return;
  }
  if (modules[asset.id] || !bundle.parent) {
    var fn = new Function('require', 'module', 'exports', asset.generated.js);
    asset.isNew = !modules[asset.id];
    modules[asset.id] = [fn, asset.deps];
  } else if (bundle.parent) {
    hmrApply(bundle.parent, asset);
  }
}
function hmrAcceptCheck(bundle, id) {
  var modules = bundle.modules;
  if (!modules) {
    return;
  }
  if (!modules[id] && bundle.parent) {
    return hmrAcceptCheck(bundle.parent, id);
  }
  if (checkedAssets[id]) {
    return;
  }
  checkedAssets[id] = true;
  var cached = bundle.cache[id];
  assetsToAccept.push([bundle, id]);
  if (cached && cached.hot && cached.hot._acceptCallbacks.length) {
    return true;
  }
  return getParents(global.parcelRequire, id).some(function (id) {
    return hmrAcceptCheck(global.parcelRequire, id);
  });
}
function hmrAcceptRun(bundle, id) {
  var cached = bundle.cache[id];
  bundle.hotData = {};
  if (cached) {
    cached.hot.data = bundle.hotData;
  }
  if (cached && cached.hot && cached.hot._disposeCallbacks.length) {
    cached.hot._disposeCallbacks.forEach(function (cb) {
      cb(bundle.hotData);
    });
  }
  delete bundle.cache[id];
  bundle(id);
  cached = bundle.cache[id];
  if (cached && cached.hot && cached.hot._acceptCallbacks.length) {
    cached.hot._acceptCallbacks.forEach(function (cb) {
      cb();
    });
    return true;
  }
}
},{}]},{},["node_modules/parcel-bundler/src/builtins/hmr-runtime.js","static/js/fatalities.js"], null)
//# sourceMappingURL=/fatalities.e22a0718.js.map