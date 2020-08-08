{
  'targets': [
    {
      	'target_name': 'binding',
        "cflags_cc": [ "-fexceptions" ],
      	'sources': [ 'cpp/makequestions.cpp' ],
      	"include_dirs" : [
			"<!(node -e \"require('nan')\")"
		]
    },
    {
      	'target_name': 'bindingA',
        "cflags_cc": [ "-fexceptions" ],
      	'sources': [ 'cpp/getanswers.cpp' ],
      	"include_dirs" : [
			"<!(node -e \"require('nan')\")"
		]
    }
  ]
}