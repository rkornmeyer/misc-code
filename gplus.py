import framework
# unique to module
import urllib2
import json

class Module(framework.module):
    
    def __init__(self, params):
        framework.module.__init__(self, params)
        self.register_option('domain', self.goptions['domain']['value'], 'yes', self.goptions['domain']['desc'])
        self.info = {
            'Name': 'Google CSE Hostname Enumerator',
            'Author': 'Tim Tomes (@LaNMaSteR53)',
            'Description': 'Leverages the Google Custom Search Engine API to harvest hosts using the \'site\' search operator and updates the \'hosts\' table of the database with the results.',
            'Comments': []
        }
    
    def module_run(self):
        domain = self.options['domain']['value']
        base_query = "https://www.googleapis.com/plus/v1/people?query=" + domain + "&alt=json&key=&maxResults=50"
        hosts = []
        new = 0
        i = 0
        ip = ''
        while True:
            query = urllib2.urlopen(base_query)
            theUglyJSON = query.read()
            jsonBlob = json.loads(theUglyJSON)
            results = jsonBlob['items']
            if not results: break
            while (i <= len(results) - 1):
                host = results[i]['displayName']
                ip = results[i]['url']
                if not host in hosts:
                    hosts.append(host)
                    self.output(host)
                    self.output(ip)
                    # add each host to the database
                    new += self.add_host(host)
                    i += 1
        self.output('%d total hosts found.' % (hosts))
        if new: self.alert('%d NEW hosts found!' % (new))
