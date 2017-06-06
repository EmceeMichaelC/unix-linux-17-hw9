from subprocess import Popen, PIPE

def service_mgmt(action, service):
    """
    service_mgmt function.  Facilitates executing commands on services
    :type action: string
    :param action: action to perform on service.
                   start, stop, restart, status
    :type service: string
    :param service: service to perform action on.
                    must be a valid linux service
    :type return: tuple
    :return tuple: (response_message, success)
                   response_message: output from the service call
                   success: boolean if command was successful
    """
    # implement actually calling the service binary using subprocess
    command = ['service', service, action]

    # execute command using Popen
    p = Popen(command, stdout=PIPE, stderr=PIPE, shell=False)
    # poll the subprocess call for data (exit code, stderr/stdout, etc.)
    while not isinstance(p.returncode, int):
        p.poll()

    sout = []
    for line in p.stdout.readlines():
        sout.append(line.strip())
    
    serr = []
    for line in p.stderr.readlines():
        serr.append(line.strip())

    statusCode = {
        0: 'success',
        1: 'notfound',
        2: 'err'
        }

    returnCode = p.returncode
    
    # successful command
    if returnCode == 0:
        status = statusCode[0]
    elif returnCode == 3:
        #check stdout to see if service is 'not found'.
        if sout[1].find('not-found') >= 0:
            status = statusCode[1]
        #check if it is loaded, but not started.
        elif sout[1].find('loaded') >= 0:
            status = statusCode[0]
    #not found
    elif returnCode == 5:
        status = statusCode[1]
    # unsuccessful command
    else:
        status = statusCode[2]

    # return results
    return ("{0}:{1} - {2}/{3}".format(action,service, sout, serr), status)
