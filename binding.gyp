{
  'targets': [
    {
      	'target_name': 'binding',
        "cflags_cc": [ "-std=c++17", "-fconcepts", "-fPIC"],
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