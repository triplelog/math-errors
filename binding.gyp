{
  'targets': [
    {
      	'target_name': 'binding',
      	"cflags": [ "-std=c++17", "-llua", "-ldl" ],
        "cflags_cc": [ "-std=c++17", "-llua", "-ldl" ],
      	'sources': [ 'cpp/main.cpp' ],
      	"include_dirs" : [
			"<!(node -e \"require('nan')\")"
		]
    }
  ]
}