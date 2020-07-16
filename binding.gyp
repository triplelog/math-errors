{
  'targets': [
    {
      	'target_name': 'binding',
        "cflags_cc": [ ],
      	'sources': [ 'cpp/nodehello.cpp' ],
      	"include_dirs" : [
			"<!(node -e \"require('nan')\")"
		]
    }
  ]
}