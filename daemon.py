import os
import signal # we need this module to send a signal to a process
import multiprocessing


# not sure if it is necessary... maybe the context of execution gives good default value
def startmethod():
    if os.name == "nt":
        startmethod = 'spawn'
    else:
        startmethod = 'fork'
        # this should provide the good starting method for our daemon process
    return(multiprocessing.set_start_method(startmethod))    


# INFO: class multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={}, *,
#daemon=None)

def duplicate_process(duplicandum):
    duplicate = multiprocessing.Process(target=duplicandum, daemon=None)
    startmethod()
    # a question here, do we join or not? Join blocks until the process finishes. We don't want that.
    # in fact we might don't want our process to terminate at all...
    return(duplicate)

def kill_parent_process():
    
    childPID = os.getpid()
    ppid = os.getppid()
    killed = os.kill(ppid,signal.CTRL_C_EVENT)
    return (print(f"Child PID:{childPID}", f"Parent PID:{ppid}",f"killed ={killed}"))


def daemonize(daemonendum):
    # maybe not necessary, just to keep in mind that there is different start method
    '''(Warning: daemon=None) from Python's doc:    
    The process’s daemon flag, a Boolean value. This must be set before start() is called.
    The initial value is inherited from the creating process.
    When a process exits, it attempts to terminate all of its daemonic child processes. (EXACTLY THE OPPOSITE OF WHAT WE WANT !!)
    Note that a daemonic process is not allowed to create child processes. Otherwise a daemonic process
    would leave its children orphaned if it gets terminated when its parent process exits. Additionally, these
    ARE NOT UNIX DAEMONS or services, they are NORMAL processes that will be terminated (and not joined) if
    non-daemonic processes have exited.'''

    # on the contrary the terminate() method is what we want: 
    '''from Python's doc:
    terminate()
    Terminate the process. On Unix this is done using the SIGTERM signal; on Windows
    TerminateProcess() is used. Note that exit handlers and finally clauses, etc., will not be executed.
    Note that descendant processes of the process WILL NOT BE TERMINATED– they will simply become orphaned. '''

    # Now we can handle the parent process by the os.kill(pid,sig) function and os.ppid() which will give us the pid
    # of the parent process after we start the child. 

    # let's duplicate the process
    daemon = duplicate_process(daemonendum) 
        # don't forget to start it
    daemon.start()
        # now we can kill the parent process
    kill_parent_process()
    #daemon.join() should we join it or not ?
    

        
        