import socket, sys, time, xml.dom.minidom, uuid
from xml.sax.saxutils import escape
from APIConstants import APIConstants
from APIVariables import APIVariables

class Utilities(object):
    
    @staticmethod
    def xmlRequest(data):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (APIVariables.ADDRESS, APIVariables.PORT)
        sock.connect(server_address);
        
        try:
            
            request = '<?xml version="1.0" encoding="utf-8"?>' + \
            '<ClientIntegrationRequest>' + \
            '<RequestUID>' + str(uuid.uuid4()) + '</RequestUID>' + \
            data + \
            '</ClientIntegrationRequest>'
            
            sock.sendall(request.encode('utf-8'))
        
            sock.settimeout(20);
            time.sleep(3)
            response = sock.recv(10025)
            
            formatted = xml.dom.minidom.parseString(response)
            pretty_xml_as_string = formatted.toprettyxml()
            print pretty_xml_as_string
        
        finally:
            
            print >>sys.stderr, 'closing socket'
            sock.close()