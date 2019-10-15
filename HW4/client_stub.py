# SKELETON CODE FOR CLIENT STUB HW4
import xmlrpclib, config, pickle

class client_stub():

    def __init__(self):
        self.proxy = xmlrpclib.ServerProxy("http://localhost:8000/")


    # DEFINE FUNCTIONS HERE

    # example provided for initialize
    def Initialize(self):
        try :
            self.proxy.Initialize()
        except Exception as err :
            # print error message
            quit()


    ''' WRITE CODE HERE '''
    def inode_number_to_inode(self, inode_number):
        try :
            inode_number = pickle.dumps(inode_number)  
            retVal = self.proxy.inode_number_to_inode(inode_number) 
            retVal = pickle.loads(retVal)
            return retVal

        except Exception as err :
            print("error message: inode_number_to_inode failed")
            quit()

    def get_data_block(self, block_number):
        try :
            block_number = pickle.dumps(block_number)
            retVal = self.proxy.get_data_block(block_number)
            retVal = pickle.loads(retVal)
            return retVal
        except Exception as err :
            print("error message: get_data_block failed")
            quit()

    def get_valid_data_block(self):
        try :
            retVal = self.proxy.get_valid_data_block()
            retVal = pickle.loads(retVal)
            return retVal
        except Exception as err :
            print("error message: get_valid_data_block failed")
            quit()


    def free_data_block(self, block_number):
        try :
            block_number = pickle.dumps(block_number)
            retVal = self.proxy.free_data_block(block_number)
            retVal = pickle.loads(retVal)  
        except Exception as err :
            print("error message: free_data_block failed")
            quit()

    def update_data_block(self, block_number, block_data):
        try :
            block_number = pickle.dumps(block_number)
            block_data = pickle.dumps(block_data)
            retVal = self.proxy.update_data_block(block_number, block_data)
            retVal = pickle.loads(retVal)  
        except Exception as err :
            print("error message: update_data_block failed")
            quit()

    def update_inode_table(self, inode, inode_number):
        try :
            inode = pickle.dumps(inode)
            inode_number = pickle.dumps(inode_number)
            retVal = self.proxy.update_inode_table(inode, inode_number)
            retVal = pickle.loads(retVal)
        except Exception as err :
            print("error message:update_inode_table failed")
            quit()

    def status(self):
        try :
            retVal = self.proxy.status()
            retVal = pickle.loads(retVal)
            return retVal
        except Exception as err :
            print("error message: status failed")
            quit()

