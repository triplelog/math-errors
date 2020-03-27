#include <nan.h>
#include <string>
#include <chrono>

#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <math.h>
#include <limits.h>
#include <time.h>
#include <string.h> 
#include <ctype.h>
#include <iostream>
#include <variant>
#include <map>
#include <numeric>
#include <chrono>
#include <thread>
#include <sstream>
#include <iostream>
#include <dlfcn.h>

#include "addition.cpp"
#include "subtraction.cpp"
#include "cppdata.cpp"

#include <lua.hpp>

void Latexify(const Nan::FunctionCallbackInfo<v8::Value>& info);

void Latexify(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	//v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	//v8::String::Utf8Value s(isolate, info[0]);
	char exp[3] = {'#','#','/'};
	std::vector<std::string> intstr;
	intstr.push_back("3");
	intstr.push_back("4");
	int size = 2;
	//std::string str(*s);
	std::string out = latexifyString(exp,intstr,size);
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(out);
	info.GetReturnValue().Set(h.ToLocalChecked());
}

void MethodAdd(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s1(isolate, info[0]);
	v8::String::Utf8Value s2(isolate, info[1]);
	std::string str1(*s1);
	std::string str2(*s2);
	
	std::vector<std::string> strs;
	strs.push_back(str1);
	strs.push_back(str2);
	std::string out = addInts(strs);
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(out);
	info.GetReturnValue().Set(h.ToLocalChecked());
}
void MethodAddWrong(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s1(isolate, info[0]);
	v8::String::Utf8Value s2(isolate, info[1]);
	v8::String::Utf8Value s3(isolate, info[2]);
	std::string str1(*s1);
	std::string str2(*s2);
	std::string str3(*s3);
	
	std::vector<std::string> strs;
	strs.push_back(str1);
	strs.push_back(str2);
	
	std::string out("temp");
	lua_State *L;
    L = luaL_newstate();

	/* load Lua base libraries */
	luaL_openlibs(L);

	/* load the script */
	luaL_dofile(L, "/home/rwilcox/math-errors/cpp/arithmetic.lua");
	/*
	void* handle = dlopen("/home/rwilcox/math-errors/cpp/arithmetic.so", RTLD_LAZY);
	if (!handle) {
        out = "no handle";
    }
    else {
    	typedef std::string (*hello_t)(std::vector<std::string>, std::string);
		hello_t hello = (hello_t) dlsym(handle, "addIntsWrongSO");
		out = hello(strs,str3);
    }*/
    
    
	
	
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(out);
	info.GetReturnValue().Set(h.ToLocalChecked());
}
void MethodSubtract(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s1(isolate, info[0]);
	v8::String::Utf8Value s2(isolate, info[1]);
	std::string str1(*s1);
	std::string str2(*s2);
	
	std::vector<std::string> strs;
	strs.push_back(str1);
	strs.push_back(str2);
	std::string out = subtractTwoInts(str1,str2);
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(out);
	info.GetReturnValue().Set(h.ToLocalChecked());
}
void MethodSubtractWrong(const Nan::FunctionCallbackInfo<v8::Value>& info) {
	v8::Isolate* isolate = info.GetIsolate();
	//v8::Local<v8::Context> context = isolate->GetCurrentContext();
	//int row = info[0]->Int32Value(context).FromJust();
	v8::String::Utf8Value s1(isolate, info[0]);
	v8::String::Utf8Value s2(isolate, info[1]);
	v8::String::Utf8Value s3(isolate, info[2]);
	std::string str1(*s1);
	std::string str2(*s2);
	std::string str3(*s3);
	
	std::vector<std::string> strs;
	strs.push_back(str1);
	strs.push_back(str2);
	
	
	
	std::string out = subtractIntsWrong(strs,str3);
	Nan::MaybeLocal<v8::String> h = Nan::New<v8::String>(out);
	info.GetReturnValue().Set(h.ToLocalChecked());
}

void Init(v8::Local<v8::Object> exports) {
  v8::Local<v8::Context> context = exports->CreationContext();
  exports->Set(context,
               Nan::New("latexify").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(Latexify)
                   ->GetFunction(context)
                   .ToLocalChecked());
  exports->Set(context,
               Nan::New("addints").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(MethodAdd)
                   ->GetFunction(context)
                   .ToLocalChecked());
  exports->Set(context,
               Nan::New("addwrong").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(MethodAddWrong)
                   ->GetFunction(context)
                   .ToLocalChecked());
  exports->Set(context,
               Nan::New("subtractints").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(MethodSubtract)
                   ->GetFunction(context)
                   .ToLocalChecked());
  exports->Set(context,
               Nan::New("subtractwrong").ToLocalChecked(),
               Nan::New<v8::FunctionTemplate>(MethodSubtractWrong)
                   ->GetFunction(context)
                   .ToLocalChecked());
}

NODE_MODULE(helloarray, Init)