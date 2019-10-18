# SKELETON CODE FOR SERVER STUB HW4
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

import time, Memory, pickle , InodeOps, config, DiskLayout


filesystem = Memory.Operations()

# FUNCTION DEFINITIONS 

# example provided for initialize
def Initialize():
    retVal = Memory.Initialize()
    retVal = pickle.dumps(retVal)
    return retVal


''' WRITE CODE HERE FOR REST OF FUNCTIONS'''

def inode_number_to_inode(inode_number):
    inode_number = pickle.loads(inode_number) #unmarshalling data
    retVal = filesystem.inode_number_to_inode(inode_number)
    retVal = pickle.dumps(retVal) # marshalling response. Same for rest of the code
    return retVal


#REQUEST THE DATA FROM THE SERVER
def get_data_block(block_number):
    block_number = pickle.loads(block_number)
    retVal = ''.join(filesystem.get_data_block(block_number))
    retVal = pickle.dumps(retVal)
    return retVal


#REQUESTS THE VALID BLOCK NUMBER FROM THE SERVER 
def get_valid_data_block():
    retVal = ( filesystem.get_valid_data_block() )
    retVal = pickle.dumps(retVal)
    return retVal


#REQUEST TO MAKE BLOCKS RESUABLE AGAIN FROM SERVER
def free_data_block(block_number):
    block_number = pickle.loads(block_number)
    filesystem.free_data_block((block_number))
    ack = pickle.dumps(1)
    return ack


#REQUEST TO WRITE DATA ON THE THE SERVER
def update_data_block(block_number, block_data):
    block_number = pickle.loads(block_number)
    block_data = pickle.loads(block_data)
    filesystem.update_data_block(block_number, block_data)
    #returning acknowledgement to finish the command
    ack = pickle.dumps(1)
    return ack


#REQUEST TO UPDATE THE UPDATED INODE IN THE INODE TABLE FROM SERVER
def update_inode_table(inode, inode_number):
    inode = pickle.loads(inode)
    inode_number = pickle.loads(inode_number)
    filesystem.update_inode_table(inode, inode_number)
    #returning acknowledgement to finish the command
    ack = pickle.dumps(1)
    return ack


#REQUEST FOR THE STATUS OF FILE SYSTEM FROM SERVER
def status():
    retVal = filesystem.status()
    retVal = pickle.dumps(retVal)
    return retVal

server = SimpleXMLRPCServer(("",8000))
print ("Listening on port 8000...")

# REGISTER FUNCTIONS

#example provided for initialize
server.register_function(Initialize,                "Initialize")

server.register_function(inode_number_to_inode,     "inode_number_to_inode")

server.register_function(get_data_block,            "get_data_block")

server.register_function(get_valid_data_block,      "get_valid_data_block")

server.register_function(free_data_block,           "free_data_block")

server.register_function(update_data_block,         "update_data_block")

server.register_function(update_inode_table,        "update_inode_table")

server.register_function(status,                    "status")
''' WRITE CODE HERE FOR REST OF REGISTER CALLS '''

# run the server
server.serve_forever()














