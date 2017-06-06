#!/usr/bin/env python
"""
flask API for controlling linux services
"""
from service_mgmt import service_mgmt
from invalidusage import InvalidUsage
from flask import Flask, abort, request, jsonify, make_response

app = Flask(__name__)
app.debug = False

allowed_actions = ['start', 'stop', 'restart']

@app.errorhandler(InvalidUsage)
def invalid_request(error):
    """
    Error Handler for invalid requests raising an
    InvalidUsage object.
    :type error: InvalidUsage
    :param error: InvalidUsage object with error data
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/v1/services/<service>', methods=['GET'])
def serviceStatus(service):
    """
    Get status of a service.
    :type service: string
    :param service: name of service.
    """
    return getResponse('status', service)

@app.route('/v1/services/<service>/<action>', methods=['PUT'])
def serviceAction(service, action):
    """
    Services API entry point
    :type action: string
    :param action: action to perform.
                   start, stop, restart
    :param service: name of service to perform action on
    """
    # quick action validation
    if not action in allowed_actions:
        abort(404)

    return getResponse(action, service)

def getResponse(action, service):
    ## make our service call ##
    
    # call service_mgmt and obtain output and return code
    try:
        (output, status) = service_mgmt(action=action, service=service)
    except Exception, err:
        # debug mode raise exception for stack trace visibility
        if app.debug:
            raise
        # set return values to failed if exception occurs
        output = "{0}".format(err)
        status = 'error'

    ## format and send our response back to client ##
    # generate our response
    resp = jsonify({'result': status, 'output': output})

    # generate appropriate response code based on status
    if status == 'success':
        resp.status_code = 200
    elif status == 'notfound':
        resp.status_code = 404
    else:
        resp.status_code = 500

    return resp

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
