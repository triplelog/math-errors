{
  'targets': [
    {
      	'target_name': 'binding',
      	"cflags": [ "-std=c++17" ],
        "cflags_cc": [ "-std=c++17", "-fPIC"],
      	'sources': [ 'cpp/main.cpp' ],
      	"libraries": [
          "-ldl",
          "-llua",
        ],
      	"include_dirs" : [
			"<!(node -e \"require('nan')\")"
		]
    }
  ]
}