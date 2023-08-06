(self["webpackChunkcustom_onnx"] = self["webpackChunkcustom_onnx"] || []).push([["lib_widget_js-webpack_sharing_consume_default_jupyter-widgets_base-webpack_sharing_consume_de-cffbaf"],{

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) nallezard
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) nallezard
// Distributed under the terms of the Modified BSD License.
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ExampleView = exports.ExampleModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base?ea51");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
//@ts-ignore
const onnxruntime_web_1 = __webpack_require__(/*! onnxruntime-web */ "webpack/sharing/consume/default/onnxruntime-web/onnxruntime-web");
const onnxruntime_web_2 = __webpack_require__(/*! onnxruntime-web */ "webpack/sharing/consume/default/onnxruntime-web/onnxruntime-web");
const jupyter_dataserializers_1 = __webpack_require__(/*! jupyter-dataserializers */ "./node_modules/jupyter-dataserializers/lib/index.js");
const ndarray = __webpack_require__(/*! ndarray */ "webpack/sharing/consume/default/ndarray/ndarray?a2eb");
// //use an async context to call onnxruntime functions.
// async function create(model_path:string) {
//     //try {
//         // create a new session and load the specific model.
//         //
//         // the model in this example contains a single MatMul node
//         // it has 2 inputs: 'a'(float32, 3x4) and 'b'(float32, 4x3)
//         // it has 1 output: 'c'(float32, 3x3)
//         env.wasm.wasmPaths='./wasm/'
//         env.wasm.numThreads=2
//         const session = await InferenceSession.create(model_path,{ executionProviders: ['wasm']});
//         console.log("create",session)
//         return session
//         // const inputnames=session.inputNames[0]
//         // // prepare inputs. a tensor need its corresponding TypedArray as data
//         // const random_data = Float32Array.from({length: 320*320*3}, () => Math.floor(Math.random() ));
//         // const tensor_in = new Tensor('float32', random_data, [1,3,320, 320]);
//         // // prepare feeds. use model input names as keys.
//         // const feeds: Record<string, any> = {};
//         // feeds[inputnames]=tensor_in
//         // // feed inputs and run
//         // const results = await session.run(feeds);
//         // // read from results
//         // const dataC = results
//         // console.log("result",dataC)
//         // el.textContent=`data of result tensor 'c': ${dataC}`;
//     // } catch (e) {
//     //     document.write(`failed to inference ONNX model: ${e}.`);
//     // }
// }
function serializeImageData(array) {
    return new DataView(array.buffer.slice(0));
}
function deserializeImageData(dataview) {
    if (dataview === null) {
        return null;
    }
    return new Uint8ClampedArray(dataview.buffer);
}
class ExampleModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: ExampleModel.model_name, _model_module: ExampleModel.model_module, _model_module_version: ExampleModel.model_module_version, _view_name: ExampleModel.view_name, _view_module: ExampleModel.view_module, _view_module_version: ExampleModel.view_module_version, value: 'Hello World', model_path: './model.onnx', initialized: false, done: false, image_data: null, array: ndarray([]), array_out: ndarray([]) });
    }
    initialize(attributes, options) {
        super.initialize(attributes, options);
        console.log("custom onnx model init");
        this.on('change:image_data', this.onImageData.bind(this));
        this.on('change:array', this.onChangeArray.bind(this));
        this.session = undefined;
        const model_path = this.get("model_path");
        console.log("model_path", model_path);
        this.create(model_path);
        console.log("session", this.session);
    }
    //use an async context to call onnxruntime functions.
    create(model_path) {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                // create a new session and load the specific model.
                //
                // the model in this example contains a single MatMul node
                // it has 2 inputs: 'a'(float32, 3x4) and 'b'(float32, 4x3)
                // it has 1 output: 'c'(float32, 3x3)
                onnxruntime_web_2.env.wasm.wasmPaths = './wasm/';
                onnxruntime_web_2.env.wasm.numThreads = 2;
                this.session = yield onnxruntime_web_1.InferenceSession.create(model_path, { executionProviders: ['wasm'] });
                console.log("create session", this.session);
                this.set("initialized", true);
                this.save_changes();
            }
            catch (e) {
                console.error(e);
            }
        });
    }
    run_model(values, shape) {
        return __awaiter(this, void 0, void 0, function* () {
            console.log("run_model with", this.session, shape);
            var feeds = {};
            // feed inputs and run
            const input_tensor = new onnxruntime_web_1.Tensor('float32', values, shape);
            feeds[this.session.inputNames[0]] = input_tensor;
            const results = yield this.session.run(feeds);
            const shape_out = results[this.session.outputNames[0]].dims;
            const data_out = results[this.session.outputNames[0]].data;
            // console.log("data_out",data_out)
            // console.log("shape_out",shape_out)
            const array_out = ndarray(data_out, shape_out);
            console.log("ndarray out", array_out);
            this.set("array_out", array_out);
            this.set("done", true);
            this.save_changes(this.callbacks());
        });
    }
    onChangeArray() {
        console.log("onArray");
        this.set("done", false);
        this.save_changes(this.callbacks());
        const array = this.get("array");
        console.log("array_data", array.data, array.shape); //,array_data.buffer.buffer)
        this.run_model(array.data, array.shape);
        console.log("fin");
    }
    onImageData() {
        console.log("onImageData");
        const data = this.get("image_data");
        const float_data = Float32Array.from(data);
        console.log("data float", float_data);
        //const tensorA = new Tensor('float32', float_data, [3, 4]);
    }
}
exports.ExampleModel = ExampleModel;
ExampleModel.serializers = Object.assign(Object.assign({}, base_1.DOMWidgetModel.serializers), { image_data: {
        serialize: serializeImageData,
        deserialize: deserializeImageData
    }, array: jupyter_dataserializers_1.compressed_array_serialization, array_out: jupyter_dataserializers_1.compressed_array_serialization });
ExampleModel.model_name = 'ExampleModel';
ExampleModel.model_module = version_1.MODULE_NAME;
ExampleModel.model_module_version = version_1.MODULE_VERSION;
ExampleModel.view_name = 'ExampleView'; // Set to null if no view
ExampleModel.view_module = version_1.MODULE_NAME; // Set to null if no view
ExampleModel.view_module_version = version_1.MODULE_VERSION;
class ExampleView extends base_1.DOMWidgetView {
    render() {
        this.el.classList.add('custom-widget');
        this.value_changed();
        this.model.on('change:value', this.value_changed, this);
        //
    }
    value_changed() {
        this.el.textContent = this.model.get('value');
        console.log("on value changed", this.model.get("array_out"));
        //let arr= ndarray(new Float64Array([1, 0, 0, 1]), [2,2])
        // console.log("arr ndarray",arr)
        // //const a={ shape: [2,2], dtype:'float32', buffer: arr.data as ndarray.TypedArray }
        // this.model.set("array_out",arr)
        // this.touch()
    }
}
exports.ExampleView = ExampleView;
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".custom-widget {\n  background-color: lightseagreen;\n  padding: 0px 2px;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"custom_onnx","version":"0.1.0","description":"A Custom Jupyter Widget Library","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/myorg/custom_onnx","bugs":{"url":"https://github.com/myorg/custom_onnx/issues"},"license":"BSD-3-Clause","author":{"name":"nallezard","email":"nicolas.allezard@cea.fr"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/myorg/custom_onnx"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf custom_onnx/labextension","clean:nbextension":"rimraf custom_onnx/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2 || ^3 || ^4 || ^5 || ^6","jupyterlab-datawidgets":"^7.1.2","ndarray":"^1.0.19","onnxruntime-web":"^1.8.0"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyter-widgets/base-manager":"^1.0.2","@jupyterlab/builder":"^3.0.0","@lumino/application":"^1.6.0","@lumino/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/ndarray":"^1.0.11","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","copy-webpack-plugin":"^8.1.1","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"custom_onnx/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js-webpack_sharing_consume_default_jupyter-widgets_base-webpack_sharing_consume_de-cffbaf.1571372a5320031d5537.js.map