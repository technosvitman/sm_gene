# statemachine

## Introduction

In many microcontroler programs, without the help of tiny OS (like FreeRTOS), we need to implement a non-blocking state machine.
In many programs we just can see the easy way, which will be quite difficult to maintain afterwards : a switch/case called each time in the main loop.
This generator build state machine using the library [statemachine](https://github.com/technosvitman/statemachine)

## What is a state ?

A state is described by 3 actions: 

* *on_enter* : what to do on enter
* *do_job* : what to do on *event*
* *on_exit* : what to do on exit

Switching from a state to another is managed by *do_job* regarding which *event* is recieved. 

## What is an event ?

An event is identified by an integer value and sometimes has attached data.
For example, an event can be "button pushed" and the attached data can be "the button identifier"

## Generator your state machine

This lib integrate a generator to build code basis to build your own state machine.

The input is a YAML file that describe the machine.

The output files are : 

* *.c file : the source code 
* *.h file : the header
* *.plantuml : UML diagramme in plantuml format
* *.png : UML diagramme

These files are stored into generator/output directory

### Describe your state machine

```yaml

{
    "machine" : "", # your state machine name
    
    "entry" : "", # the entry point state name

    "global" : # global state action 
    {
        "actions" : [], #see states
        "enter" : "", #see states 
        "exit" : "", #see states
    }
    
    # the states list
    states : 
    [
        { 
            "name" : "", # sthe state name
            "comment" : "", # some information on the state

            # describes state change and/or action on a event
            "actions" : 
            [
                # an action
                { 
                    "to" : "", # destination state name
                    "events" : 
                    [   # the list of events triggering the state change
                        { 
                            "name" : "", #the event name
                            "comment" : "" # optional event description. You can set only one time the event comment
                        },
                        #another event
                        {
                            ...
                        }
                    ],
                    "job" : "" # what to do on this event
                },
                # another action
                {
                    ...
                }
            ],
        },
        # an other state
        {
             ...
        }
    ]
}

```


### Build your machine

Call the generator like this from the generator directory : 

```
    python StateMachineGenerator.py -i {path_to_your YAML file}
```

It stored automaticaly output files with the base name of yout yaml file

You can set a custom output name with the '-o' option

```
    python SMGene.py -i {path_to_your YAML file} -o {your_custom_name}
 ```

### Apply your file template

You can describe templates to build the state machine. 

You will find exemples in *templates* directory :
* [default source template](templates/template_source.c)
* [default header template](templates/template_header.h)

Availables templates are for source and header files.

#### Source template

filename to use : *template_source.c*

In the source you may put : 

* _$statemachine_includes_ : where the modules includes should be inserted
* _$statemachine_states_dcl_ : where private states callbacks declaration should be inserted
* _$statemachine_globales_ : where modules globales variables should be inserted
* _$statemachine_states_clbk_ : where private states callbacks implementation should be inserted
* _$statemachine_states_ : where states declaration should be inserted ( has to be after states callbacks )
* _$statemachine_func_ : where public function should be inserted

#### Header template

filename to use : *template_header.c*

In the source you may put : 

* _$statemachine_begin_ : where the header content should begin
* _$statemachine_types_ : where the machine types should be inserted
* _$statemachine_func_ : where public function should be inserted

#### Generation

Put templates in a directory and start generation with : 

```
    python SMGene.py -i {path_to_your YAML file} -o {your_custom_name} -t {your_template_directory}
 ```
  
### Example

You can find the state machine example here : 

* [description](machine_example.yml)
* [source](output/machine_example.c)
* [header](output/machine_example.h)
* [plantuml](output/machine_example.plantuml)
* [uml](output/machine_example.png)
  


