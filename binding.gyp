{
  'targets': [
    {
      	'target_name': 'binding',
        "cflags_cc": [ ],
      	'sources': [ 'cpp/nodematherrors.cpp' ],
      	"include_dirs" : [
			"<!(node -e \"require('nan')\")"
		]
    }
  ]
}