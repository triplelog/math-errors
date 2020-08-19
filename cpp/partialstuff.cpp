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

void Hello(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	//v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	//v8::String::Utf8Value s(isolate, info[0]);
	//std::string str(*s);
	jsonmessage = "var rule = {};";
	srand(time(NULL));
	initialRun();
	
	//makeInt("[10,12)U((0,5)U[4,6]U(8,10])");
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(jsonmessage);
	info.GetReturnValue().Set(h.ToLocalChecked());
}

void OneRule(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string a(*s);
	
	
	
	
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(a);

	
	info.GetReturnValue().Set(h.ToLocalChecked());
}

void LatexIt(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s(isolate, info[0]);
	std::string a(*s);
	
	std::cout << "input: " << a <<"\n";
	std::string postfixed = postfixify(a);
	std::cout << "postfixed: " << postfixed <<"\n";
	std::string latexed = latexOne(postfixed);
	std::cout << "latexed: " << latexed <<"\n";
	
	
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(latexed);

	
	info.GetReturnValue().Set(h.ToLocalChecked());
}


void Init(v8::Local<v8::Object> exports) {
  v8::Local<v8::Context> context = exports->CreationContext();
  exports->Set(context,
               Nan::New("hello").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(Hello)
                   ->GetFunction(context)
                   .ToLocalChecked());
  exports->Set(context,
               Nan::New("onerule").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(OneRule)
                   ->GetFunction(context)
                   .ToLocalChecked());
  exports->Set(context,
               Nan::New("latexify").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(LatexIt)
                   ->GetFunction(context)
                   .ToLocalChecked());

}

NODE_MODULE(helloarray, Init)