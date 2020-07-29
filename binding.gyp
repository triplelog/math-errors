{
  'targets': [
    {
      	'target_name': 'binding',
        "cflags_cc": [ "-fexceptions" ],
      	'sources': [ 'cpp/parallelmain.cpp' ],
      	"include_dirs" : [
			"<!(node -e \"require('nan')\")"
		]
    }
  ]
}