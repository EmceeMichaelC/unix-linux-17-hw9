# unix-linux-17-hw9
Unix Linux Q3 2017 HW9

## Updates

## app.py
* updated routes
  * GET /v1/services/<service>  -- retrieve status for a service.
  * PUT /v1/services/<service>/<action> -- for a service, perform an action: start, stop, restart
* added handling of status from service_mgmt output to return 404 for 'notfound'. 

### service_mgmt.py implementation
* added Popen implementation to call /usr/bin/service.
* added error handling of different exit codes of /usr/bin/service, including 3 (service not found or stopped), 5 (service not found).
* changed output: tuple of (response_message, status)
  * response_message - output from the /usr/sbin/service call.  eg:  * Stopping web server apache2 *
  * status - 'success', 'notfound', or 'err'


### Restful HTTP Methods

Valid HTTP methods:
* GET - status calls
* PUT - start, stop, and restart calls

### Examples

* see the status of the apache2 daemon:
```
$ curl -i -X GET http://127.0.0.1:8080/v1/services/apache2
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 363
Server: Werkzeug/0.12.2 Python/2.7.12
Date: Tue, 06 Jun 2017 18:16:58 GMT

{
  "output": "status:apache2 - ['\\xe2\\x97\\x8f apache2.service - LSB: Apache2 web server', 'Loaded: loaded (/etc/init.d/apache2; bad; vendor preset: enabled)', 'Drop-In: /lib/systemd/system/apache2.service.d', '\\xe2\\x94\\x94\\xe2\\x94\\x80apache2-systemd.conf', 'Active: inactive (dead)', 'Docs: man:systemd-sysv-generator(8)']/[]",
  "result": "success"
}
```

* restart the sshd daemon:
```
$ curl -i -X PUT http://127.0.0.1:8080/v1/services/sshd/restart
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 63
Server: Werkzeug/0.12.2 Python/2.7.12
Date: Tue, 06 Jun 2017 19:43:58 GMT

{
  "output": "restart:sshd - []/[]",
  "result": "success"
}
```

* stop the cron daemon:
```
$ curl -i -X PUT http://127.0.0.1:8080/v1/services/cron/stop
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 60
Server: Werkzeug/0.12.2 Python/2.7.12
Date: Tue, 06 Jun 2017 19:53:22 GMT

{
  "output": "stop:cron - []/[]",
  "result": "success"
}
```

* bad service
```
$ curl -i -X GET http://127.0.0.1:8080/v1/services/foo
HTTP/1.0 404 NOT FOUND
Content-Type: application/json
Content-Length: 175
Server: Werkzeug/0.12.2 Python/2.7.12
Date: Tue, 06 Jun 2017 19:54:33 GMT

{
  "output": "status:foo - ['\\xe2\\x97\\x8f foo.service', 'Loaded: not-found (Reason: No such file or directory)', 'Active: inactive (dead)']/[]",
  "result": "notfound"
}
```


