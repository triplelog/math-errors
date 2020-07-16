{
  'targets': [
    {
      	'target_name': 'binding',
        "cflags_cc": [ ],
      	'sources': [ 'cpp/matherrors.cpp' ],
      	"include_dirs" : [
			"<!(node -e \"require('nan')\")"
		]
    }
  ]
}