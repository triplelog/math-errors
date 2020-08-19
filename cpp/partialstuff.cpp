#include <nan.h>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <math.h>
#include <limits.h>
#include <time.h>
#include <string.h> 
#include <ctype.h>
#include <cmath>
#include <iostream>
#include <fstream>
#include <variant>
#include <map>
#include <numeric>
#include <chrono>
#include <thread>
#include <sstream>
#include <array>
#include <vector>
#include <unistd.h>
#include <thread>
#include <future>
#include "rapidcsv.h"
#include "ctpl/ctpl_stl.h"
#include "parallel_hashmap/phmap.h"


using namespace std::chrono;
using phmap::flat_hash_map;

#include "commonstuff.cpp"

void OneRule(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string a(*s);
	
	
	
	
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(a);

	
	info.GetReturnValue().Set(h.ToLocalChecked());
}


void Init(v8::Local<v8::Object> exports) {
  v8::Local<v8::Context> context = exports->CreationContext();
  exports->Set(context,
               Nan::New("onerule").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(OneRule)
                   ->GetFunction(context)
                   .ToLocalChecked());

}

NODE_MODULE(helloarray, Init)