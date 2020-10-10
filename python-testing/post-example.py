import urllib2, base64
data = '{}'
url = 'http://192.168.0.210/dyn'
req = urllib2.Request(url, data, {'Content-Type': 'application/x-www-form-urlencoded'})
base64string = base64.b64encode('%s:%s' % ('api', 'apiuser123'))
req.add_header("Authorization", "Basic %s" % base64string)
f = urllib2.urlopen(req, "login=&username=door&password=<ThePassword>&button=Open+Door")
#for x in f:
#    print(x)
#f.close()

# curl -d "login=&username=door&password=<ThePassword>&button=Open+Door" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://192.168.0.210/dyn
# data = '{"nw_src": "10.0.0.1/32", "nw_dst": "10.0.0.2/32", "nw_proto": "ICMP", "actions": "ALLOW", "priority": "10"}'

#import urllib2, base64
#data = '{}'
#url = 'http://172.26.182.70:30100/api/v2/risks/vulnerabilities/csv'
#req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
#base64string = base64.b64encode('%s:%s' % ('api', 'apiuser123'))
#req.add_header("Authorization", "Basic %s" % base64string)
#f = urllib2.urlopen(req)
#for x in f:
#    print(x)
#f.close()

# curl -d "login=&username=door&password=<ThePassword>&button=Open+Door" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://192.168.0.210/dyn
# data = '{"nw_src": "10.0.0.1/32", "nw_dst": "10.0.0.2/32", "nw_proto": "ICMP", "actions": "ALLOW", "priority": "10"}'
