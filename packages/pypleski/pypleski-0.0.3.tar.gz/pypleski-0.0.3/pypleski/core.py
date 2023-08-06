import http.client
import ssl
import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
import json
import xmltodict


###TODO fix json outpu, implement error handling
class PleskResponsePacket():
    """ PleskResponsePacket Class provides an easy way to read responses Packets from the PLESK XML API    

    Args:
        response_xml (string): Takes the response string from PleskClient.request()
        
    
    Use examples:

        request_packet = PleskRequestPacket("webspace", "add", webhosting = {"gen_setup":{'...':'...'}, "hosting": {'...':'...'}})  

        response = PleskApiClient.request(request_packet.to_string())


        response_packet = PleskResponsePacket(response)

        response_json = response_packet.to_JSON()

        response_dict = response_packet.to_dict()

        response_list = response_packet.to_list()
        
    """
    m_error = True

    def __init__(self, response_xml):
       
        self.packet = ET.fromstring(response_xml)        
        self.result = self.packet.find(".//result")
        err = self.result.find(".//errcode")
        if err is None:                             
            self.m_error = False            

    def to_JSON(self) -> str:    ### easy to use with a JSON string        
        """ 
        Returns:
            str: Response as JSON string
        """
        return json.dumps(xmltodict.parse(self.to_string()))

    def to_dict(self) -> dict:    ### easy to use as dictionary
        """ 
        Returns:
            dict: Response as dict
        """
        return xmltodict.parse(self.to_string())

    def to_list(self) -> list :    ### only usefull for few responses due to its structure
        """ 
        Returns:
            list: Response as string list
        """
        return ET.tostringlist(self.packet, encoding="UTF-8")

    def to_string(self) -> str:    ### get the plain XML String
        """ 
        Returns:
            str: Response as XML string
        """
        return ET.tostring(self.packet, encoding="UTF-8")

    def as_xml_etree_element(self) -> ET.Element:
        """
        Returns:
            xml.etree.ElementTree.Element: The response as xml.etree.ElementTree.Element object
        """
        return self.packet
        

    @property
    def is_error(self) -> bool:   ### see if it is an error before parsing any output
        """
        Returns:
            bool: True if response contains an error
        """
        return self.m_error


### get, set, del operations all have the same pattern:
#        packet/ module / operation / filter 
### other operations are less predictable
class PleskRequestPacket():        
    """ PleskRequestPacket Class provides an easy way to create PLESK XML API requests
        
        Use examples:

        packet = PleskRequestPacket("webspace", "get", filter={"owner-id":5})

        PleskApiClient.request(packet.to_string())

        packet2 = PleskRequestPacket("webspace", "add", webhosting = {"gen_setup":{'d':'d'}, "hosting": {'d':'d'}})    

        PleskApiClient.request(packet2.to_string())


        More practical a :  

        def add_customer(self, cname, pname, login, passwd) -> PleskResponsePacket:

            request = PleskRequestPacket("customer","add", gen_info = { 
                'cname': cname, 
                'pname': pname,
                'login': login,
                'passwd': passwd,
                'status': 0,
                'phone': '',
                'fax': '',
                'email': '',
                'address': '',
                'city':'',
                'state':'',
                'pcode':'',
                'country':''
                })


        or something like: 
            customer_del = PleskRequestPacket("customer","del", filter = { 'login': 'login'})
    """

    def __init__(self, module:str ="webspace", operation:str = "get", **data) -> None:                                
        self.packet = ET.Element('packet')                
        self.module = ET.SubElement(self.packet,module)
        self.operation = ET.SubElement(self.module,operation)        
        self.filter = None                
        self.set_packet_version()
        self.setup(**data)



    def setup(self, **data):
        """Called by __init__ """
        if self.operation.tag in ["get","set","del"] and "filter" in data.keys():           
            self.add_filter(**data["filter"])
        else:
            self.add_data_to_node(self.operation, **data)         


    def set_packet_version(self, version:str="1.6.7.0"):
        """Sets the packet version for the request

        Args:
            version (str, optional): Defaults to "1.6.7.0".
        """
        
        self.packet.set("version", version)


    def add_data_to_node(self,parent, **data):    
        """Adds all data sets to the given parent Element"""
        if self.operation.tag in ["get","set","del"] and self.filter is None:
            print(f" Cant add Data {data} when craftin a {self.operation.tag} request when no filter is set. Use add_filter() to add a filter first.")
            return   
        for key, value in data.items(): 
            ## Python doesn't allow var names to have dashs 
            # if key contains substring "_id" replace it with "-id"            
            key = key.replace("_id","-id")                                            
            e = ET.SubElement(parent, key)            
            if type(value) == dict:
                self.add_data_to_node(e,**value) #recursion if we have another dict
            else:
                e.text = f"{value}"       


    def add_filter(self, **filter):
        """Adds a filter for a single get, set or del request"""
        if self.operation.tag not in ["get","set","del"]:
            print(f" Cant add Filter {filter} when craftin a {self.operation.tag} request. Use add_data_to_node() instead.")
            return
        elif self.filter is None: ### make sure filter is set when needed
            self.filter = ET.SubElement(self.operation,'filter')
        for key, value in filter.items():            
            ## Python doesn't allow var names to have dashs 
            # if key contains substring "_id" replace it with "-id"            
            key = key.replace("_id","-id")                                   
            e =ET.SubElement(self.filter, key)
            e.text = f"{value}"


    def to_string(self, encoding="UTF-8") -> str:
        """returns the packet XML as a string"""
        return ET.tostring(self.packet,encoding=encoding)
    


class PleskApiClientDummy():
    ### Just for testing purpose
    # no real connection 
    # import PleskApiClass from third_party/ for real use

    def request(self, blubb, error = False) -> str:
        return """<packet>
                        <webspace>
                            <get>
                                <result>
                                    <status>error</status>
                                    <errcode>1013</errcode>
                                    <errtext>Object not found.</errtext>
                                    <id>1234</id>
                                </result>
                            </get>
                        </webspace>
                    </packet>""" if error else """
                        <packet version="1.6.7.0">
                            <customer>
                                <add>
                                    <result>
                                        <status>ok</status>
                                        <id>3</id>
                                        <guid>d7914f79-d089-4db1-b506-4fac617ebd60</guid>
                                    </result>
                                </add>
                            </customer>
                        </packet>"""





class PleskApiClient:
    """ Simple Plesk Api Client by the PLESK Team
        https://github.com/plesk/api-examples/blob/master/python3/plesk_api_client.py        
    """

    def __init__(self, host, port = 8443, protocol = 'https', ssl_unverified = False):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.secret_key = None
        self.ssl_unverified = ssl_unverified

    def set_credentials(self, login, password):
        self.login = login
        self.password = password

    def set_secret_key(self, secret_key):
        self.secret_key = secret_key

    def request(self, request):
        headers = {"Content-type": "text/xml", "HTTP_PRETTY_PRINT": "TRUE"}
        if self.secret_key:
            headers["KEY"] = self.secret_key
        else:
            headers["HTTP_AUTH_LOGIN"] = self.login
            headers["HTTP_AUTH_PASSWD"] = self.password

        if self.protocol == 'https':
            if self.ssl_unverified:
                conn = http.client.HTTPSConnection(self.host, self.port, context=ssl._create_unverified_context())
            else:
                conn = http.client.HTTPSConnection(self.host, self.port)
        else:
            conn = http.client.HTTPConnection(self.host, self.port)
            print("! DANGER: Connection not encrypted !")

        conn.request("POST", "/enterprise/control/agent.php", request, headers) 
        response = conn.getresponse()
        data = response.read()
        return data.decode("utf-8") 
        
        
        
def obtain_plesk_session_token(user, password, ip) -> str:
    request = PleskRequestPacket("server", "create_session", login=user,data={'user_ip':ip, 'source_server':''})
    print(request.to_string())
    api = PleskApiClient(ip)
    api.set_credentials(user,password)
    try:
        response = api.request(request.to_string())
        response = PleskResponsePacket(response).to_dict()[0]
    except Exception:        
        response = False ### replace with proper error handling 
    finally:
        return response
    

def generate_password(length:int=16):
    pw = ''.join((chr(random.randint(0,255))) for _ in range(length))
    return (f"^{base64.encodestring(pw.encode('UTF-8')).strip().decode('UTF-8')}").replace('=',f"{(chr(random.randint(33,152)))}")

