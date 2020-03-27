{
  'targets': [
    {
      	'target_name': 'binding',
      	"cflags": [ "-std=c++17" ],
        "cflags_cc": [ "-std=c++17"],
        "ldflags": [ "-llua", "-ldl" ],
      	'sources': [ 'cpp/main.cpp' ],
      	"include_dirs" : [
			"<!(node -e \"require('nan')\")"
		]
    }
  ]
}