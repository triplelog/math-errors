{
  'targets': [
    {
      	'target_name': 'binding',
        "cflags_cc": [ "-std=c++17", "-O2"],
      	'sources': [ 'cpp/main.cpp' ],
      	"include_dirs" : [
			"<!(node -e \"require('nan')\")"
		]
    }
  ]
}