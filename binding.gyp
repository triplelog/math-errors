{
  'targets': [
    {
      	'target_name': 'binding',
        "cflags_cc": [ "-fexceptions", "-O3" ],
      	'sources': [ 'cpp/nodematherrors.cpp' ],
      	"include_dirs" : [
			"<!(node -e \"require('nan')\")"
		]
    }
  ]
}