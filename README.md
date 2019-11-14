# metaproject-MK-II
Second version of python projects with multiple frontends

## usage ##
call python make.py |projectname| to build a project named |projectname| from the template. 
The result is a single .py file that is a zipped version of the template, with the |template| replaced by
the given name. You can execute it by calling python |projectname|.py, or unzip it and modify it.
 
## about ##
Here is the Idea:
[I have no idea if this is gonna work...]

### backend ###
We need a backend framework that accepts commands and sends responses.
The backend might pass work to subworker threads or do the work by itself.
The backend communicates via signals and slots, so it can live in its own thread.

### frontend ###
The frontend is a separate thread that comes in one of several forms:

* A cli interface that converts cli inputs to a command queue and sends the corresponding signals one after the other.
* A gui that fetches all available commands from the backend and displays them in list form, allowing the user to execute them
* A hand-built, "rich client" GUI
* A small tcp server, that converts json-dicts sent/recvd via tcp to signals / slots and can be used to integrate the project code into an external automation system.

### differences to the qtwidgets-metaproject ###
* We scrap the automatically created latex-docu
* We scrap the pyinstaller exe-stuff.