// Copyright (c) nallezard
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';
//@ts-ignore

import {InferenceSession,Tensor} from "onnxruntime-web";
import { env } from "onnxruntime-web";

import {
 compressed_array_serialization
} from 'jupyter-dataserializers';

import ndarray = require("ndarray");

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
function serializeImageData(array: Uint8ClampedArray) {
  return new DataView(array.buffer.slice(0));
}

function deserializeImageData(dataview: DataView | null) {
  if (dataview === null) {
    return null;
  }

  return new Uint8ClampedArray(dataview.buffer);
}

export class ExampleModel extends DOMWidgetModel {
  
  session:any
  from_ts:boolean;

  defaults() {
    return {
      ...super.defaults(),
      _model_name: ExampleModel.model_name,
      _model_module: ExampleModel.model_module,
      _model_module_version: ExampleModel.model_module_version,
      _view_name: ExampleModel.view_name,
      _view_module: ExampleModel.view_module,
      _view_module_version: ExampleModel.view_module_version,
      value: 'Hello World',
      model_path:'./model.onnx',
      initialized:false,
      done:false,
      image_data:null,
      array:ndarray([]),
      array_out:ndarray([])
    };
  }
 
 static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    image_data: {
      serialize: serializeImageData,
      deserialize: deserializeImageData
    },
    array:compressed_array_serialization,
    array_out:compressed_array_serialization
    
  };
 

  static model_name = 'ExampleModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'ExampleView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;


  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    console.log("custom onnx model init")
    this.on('change:image_data', this.onImageData.bind(this));
    this.on('change:array', this.onChangeArray.bind(this));
    this.session=undefined;
    const model_path=this.get("model_path")
    console.log("model_path",model_path)
    this.create(model_path)
    console.log("session",this.session) 
  }  


//use an async context to call onnxruntime functions.
  async  create(model_path:string) {
      try {
          // create a new session and load the specific model.
          //
          // the model in this example contains a single MatMul node
          // it has 2 inputs: 'a'(float32, 3x4) and 'b'(float32, 4x3)
          // it has 1 output: 'c'(float32, 3x3)
          env.wasm.wasmPaths='./wasm/'
          env.wasm.numThreads=2
          this.session = await InferenceSession.create(model_path,{ executionProviders: ['wasm']});

          console.log("create session",this.session)
          this.set("initialized",true)
          this.save_changes()
        } catch (e) {
        console.error(e);
    }
  }

  async run_model(values : Float32Array,shape:[]){

    console.log("run_model with",this.session,shape)
    var feeds: Record<string, any> = {};
    // feed inputs and run
    const input_tensor= new Tensor('float32', values, shape);

    feeds[this.session.inputNames[0]]=input_tensor

    const results = await this.session.run(feeds);

​    const shape_out=results[this.session.outputNames[0]].dims
    const data_out=results[this.session.outputNames[0]].data
    // console.log("data_out",data_out)
    // console.log("shape_out",shape_out)
    const array_out= ndarray(data_out, shape_out)
    console.log("ndarray out",array_out)
    this.set("array_out",array_out)
    this.set("done",true)
    this.save_changes(this.callbacks())
  }


 onChangeArray(){
    console.log("onArray")
    this.set("done",false)
    this.save_changes(this.callbacks())

    const array=this.get("array")
    console.log("array_data",array.data,array.shape)//,array_data.buffer.buffer)
  
     this.run_model(array.data,array.shape)
     console.log("fin")
  
  }


  onImageData(){
    console.log("onImageData")
    const data=this.get("image_data")
    const float_data = Float32Array.from(data)
    console.log("data float",float_data)


    //const tensorA = new Tensor('float32', float_data, [3, 4]);
  }
}

export class ExampleView extends DOMWidgetView {
  render() {
    this.el.classList.add('custom-widget');

    this.value_changed();
    this.model.on('change:value', this.value_changed, this);
    //
  }
 
  value_changed() {
    this.el.textContent = this.model.get('value');
    console.log("on value changed",this.model.get("array_out"))
    //let arr= ndarray(new Float64Array([1, 0, 0, 1]), [2,2])
    // console.log("arr ndarray",arr)
    // //const a={ shape: [2,2], dtype:'float32', buffer: arr.data as ndarray.TypedArray }
    // this.model.set("array_out",arr)
    // this.touch()
  }
}
