from .core import PleskApiClientDummy
from .core import PleskRequestPacket
from .core import PleskResponsePacket
import base64
import random

class PleskCustomerManager():        
    """
        Example Manager Class for the Customer module of the PLESK XML API\n         
        Args:
            plesk (PleskApiClient, optional): The PleskApiClient Object to run requests Defaults to PleskApiClientDummy().
       
        Test Scenarios succeeded:\n
            manager = PleskCustomerManager()\n
            manager.add_customer("cname","pname","login","passwd")\n
            manager.delete_customer("login")            
    """
    def __init__(self,   plesk = PleskApiClientDummy()) -> None:       
          self.plesk = plesk

    def add_customer(self, cname, pname, login, passwd, **data) -> PleskResponsePacket:        
        """ Add a customer 

        Args:
            cname (str): company name
            pname (str): full name
            login (str): login name
            passwd (str): login passwd - has to match the password policy of your plesk server\n
            **data (dict): other user data as key:value pairs             

        Returns:
            PleskResponsePacket: Plesk APIs response PleskResponsePacket object
        """
        request = PleskRequestPacket("customer","add", gen_info = { 
            'cname': cname, 
            'pname': pname,
            'login': login,
            'passwd': passwd,
            'status': 0,
            'phone': data["phone"] if 'phone' in data.keys() else '',
            'fax': data["fax"] if 'fax' in data.keys() else '',
            'email': data["email"] if 'email' in data.keys() else '',
            'address': data["address"] if 'address' in data.keys() else '',
            'city':data["city"] if 'city' in data.keys() else '',
            'state':data["state"] if 'state' in data.keys() else '',
            'pcode':data["pcode"] if 'pcode' in data.keys() else '',
            'country':data["country"] if 'country' in data.keys() else '',
            'external-id': data["external-id"] if 'external-id' in data.keys() else '',
            'phone': data["description"] if 'description' in data.keys() else ''
            })                
        return self.do_REQUEST(request)
    
    def get_customer_info(self, login:str, dataset:str="gen_info") -> PleskResponsePacket:     
        """ Get customer info by login name

        Args:
            login (str): customers login name\n
                        
            dataset (str): use if you want to retrieve a specific dataset like "gen_info"\n

        Returns:
            PleskResponsePacket: Plesk API Response
        """         
        request =  PleskRequestPacket("customer", "get", filter={'login': login})          
        request.add_data_to_node(request.operation,  dataset={dataset:''}) # the second arguments value will create <dataset><[dataset] /> </dataset>
        return self.do_REQUEST((request))

    
    def update_customer_info(self, login, dataset) -> PleskResponsePacket:       
        pass

    def delete_customer(self, login)  -> PleskResponsePacket:   
        """Delete a customer by their login name

        Args:
            login (str): customers login name

        Returns:
            PleskResponsePacket: Response from Plesk
        """        
        request = PleskRequestPacket("customer","del", filter = { 'login': login })
        return self.do_REQUEST(request)
        

    def do_REQUEST(self, request) -> PleskResponsePacket:              
        return PleskResponsePacket(self.plesk.request(request.to_string()))

  



class PleskSubscriptionManager():        
    """
        Example Manager Class for the Webspace module of the PLESK XML API\n         
        Args:
            plesk (PleskApiClient, optional): The PleskApiClient Object to run requests Defaults to PleskApiClientDummy().  
        
        TODO \n
        Fix methods        
    """
    def __init__(self,   plesk = PleskApiClientDummy()) -> None:       
          self.plesk = plesk

    def add_subscription(self, id, domain, package, **data) -> PleskResponsePacket:        
        request = PleskRequestPacket()                    
        return self.do_REQUEST(request)
    
    def get_subscription(self, owner:str, dataset:str="gen_info") -> PleskResponsePacket:     
        """ Get subscription info 

        Args:
            owner (str): customers login name\n
                        
            dataset (str): use if you want to retrieve a specific dataset like "gen_info"\n

        Returns:
            PleskResponsePacket: Plesk API Response
        """         
        request =  PleskRequestPacket("webspace", "get", filter={'owner': owner})          
        request.add_data_to_node(request.operation,  dataset={dataset:''}) # the second arguments value will create <dataset><[dataset] /> </dataset>
        return self.do_REQUEST((request))

    
    def update_subscription(self, id, dataset) -> PleskResponsePacket:       
        pass

    def delete_subscription(self, login)  -> PleskResponsePacket:   
        """Delete a subscription

        Args:
            login (str): customers login name

        Returns:
            PleskResponsePacket: Response from Plesk
        """        
        request = PleskRequestPacket("webspace","del", filter = { 'login': login })
        return self.do_REQUEST(request)
        

    def do_REQUEST(self, request) -> PleskResponsePacket:              
        return PleskResponsePacket(self.plesk.request(request.to_string()))

  





