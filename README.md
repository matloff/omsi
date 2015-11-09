
##What is OMSI?##

Tools for conducting and grading examinations in a manner that is both
secure and conducive to high-quality measurement of student insight.

##Documentation##

Server Client Interaction:

Client:

For all Server interactions on the Client side, please follow the following protocol.

Coding:

If you are coding and you need an interaction from the server, here is how I set it up.
Write code in your class, your module, please do not modify Client unless you really know what you are doing. Import ServerInteractor in the class/module that requires the server interaction like this:
import Client
Now you have 2 functions available. Client.setUpServer(pPort, pHost) and Client.callFunctionOnServer(functionName)

Before you can do any interactions with the server, you need to call Client.setUpServer(pPort, pHost). The parameters are the port and the IP address provided by the professor.
Until we actually are in a position to test this in a real setting (test run) call the function like so:
Client.setUpServer(0, 0)

Now the server is configured on the client side. If you want to interact with the server now you need to do this by telling the server what function to execute. Make sure the function you are trying to execute actually
exists on the server and it is set up to be called by the client. Look at the Server section to find out how to set up the Server properly.

If everything is properly set up call:
Client.callFunctionOnServer("myFunctionName")

Currently parameters for server functions are not supported but that will change shortly (1 day or 2 tops!).

The return value of this is either True or False dependent on whether the execution of the function on the server was successful or not.

Either there was a problem when you set up the server, or the issue is more complicated, in which case I would suggest contacting me (Francois) or using your crazy coding skills to fix the issue yourself.

Running code:
For now, make sure to run "Server.py". This file does not take any arguments, just execute it, it sets up a server on localhost which starts listening.
Once that is done, just execute your Client script. Do not execute Client, it is not supposed to be executed by itself.




Server:

For all the code that is supposed to be run on the Server side, please follow the following protocol.

Coding:

If you are coding a script that is supposed to be triggered by a certain command from the client, or if you are writing something that needs to always run on the Server you need to link it to Server.py .
Server.py is the main method on the professor's machine. It should be executed by the professor once and then it is supposed to be running for the entire duration of the exam. Serve.py accepts request from clients, it lets students dump files (not yet, but eventually it will!)
and it lets students start the grading system etc.

If you are coding a class/module that is supposed to be run upon a client request please do not put your functions or any code into Server.py. Write your code in your class and then link it to Serve.py via an import. Simply add
import MyClassName
to the top of Server.py

In order for a function to be callable from a client's machine you need to explicitly add it to the function dictionary in Server.py . The function dictionary is a list of all function objects that is mapped to a string representative for the function (usually the function name)
In Server.py you ll find a variable called
gFunctionDictionary = { ... a bunch of functions ...}

Add your function to that table as follows:
'nameOfMyFunctionUNIQUE': MyCLassWhichIImported.nameOfMyFunction,

it is important that the first sting (in my example: "nameOfMyFunctionUNIQUE") is indeed unique. I would try to keep it as close to the actual name of the function, but still different from the other functions in the table.

As of right now, any functions you add to the function table will be called without passing in any parameters. In my example, at some point the program would call:
MyCLassWhichIImported.nameOfMyFunction()

This should match your actual function, so please do not make them accept parameters (I will change this soon!) .

Running:

Before running any client scripts, run Server.py . It sets up a server and it listens to the Clients.

If you added both the import and the functions to the function table, the Server Side is all set. Now just go ahead and call your function from the Client like so:
Client.callFunctionOnServer("nameOfMyFunctionUNIQUE")

(make sure your client side is correctly set up ofc, please refer to the Client section)
