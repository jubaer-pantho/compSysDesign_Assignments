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
            self.proxy.inode_number_to_inode(inode_number)
        except Exception as err :
            # print error message
            quit()

    def get_data_block(self, block_number):
        try :
            self.proxy.get_data_block(block_number)
        except Exception as err :
            # print error message
            quit()

    def get_valid_data_block(self):
        try :
            self.proxy.get_valid_data_block()
        except Exception as err :
            # print error message
            quit()


    def free_data_block(self, block_number):
        try :
            self.proxy.free_data_block(block_number)
        except Exception as err :
            # print error message
            quit()

    def update_data_block(self, block_number, block_data):
        try :
            self.proxy.update_data_block(block_number, block_data)
        except Exception as err :
            # print error message
            quit()

    def update_inode_table(self, inode, inode_number):
        try :
            self.proxy.update_inode_table(inode, inode_number)
        except Exception as err :
            # print error message
            quit()

    def status(self):
        try :
            self.status()
        except Exception as err :
            # print error message
            quit()

