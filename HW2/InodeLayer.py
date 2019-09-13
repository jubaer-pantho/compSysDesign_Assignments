import datetime, sys, time, config, BlockLayer, InodeOps, MemoryInterface


MemoryInterface.Initialize_My_FileSystem()
#HANDLE OF BLOCK LAYER
interface = BlockLayer.BlockLayer()



class Operations():
    def __init__(self):
        self.map = []

    #WRITES STRING1
    def write(self, string):
        data_array = []
        # verify that string is of type string
        for i in range(0, len(string), config.BLOCK_SIZE):
            # divide up the string into chunks of length BLOCK_SIZE
            data_array.append(string[i : i + config.BLOCK_SIZE])
        self.__write_to_filesystem(data_array)


    #READS THE STRING
    def read(self):
        data = []
        for i in range(len(self.map)):
            # index through block numbers in map to get data blocks
            data.append(interface.BLOCK_NUMBER_TO_DATA_BLOCK(self.map[i]))
        print( "".join(data))
        return "".join(data)

class InodeLayer():

    #PLEASE DO NOT MODIFY THIS
    #RETURNS ACTUAL BLOCK NUMBER FROM RESPECTIVE MAPPING  
    def INDEX_TO_BLOCK_NUMBER(self, inode, index):
        if index == len(inode.blk_numbers): return -1
        return inode.blk_numbers[index]


    #PLEASE DO NOT MODIFY THIS
    #RETURNS BLOCK DATA FROM INODE and OFFSET
    def INODE_TO_BLOCK(self, inode, offset):
        index = offset / config.BLOCK_SIZE
        block_number = self.INDEX_TO_BLOCK_NUMBER(inode, index)
        if block_number == -1: return ''
        else: return interface.BLOCK_NUMBER_TO_DATA_BLOCK(block_number)


    #PLEASE DO NOT MODIFY THIS
    #MAKES NEW INODE OBJECT
    def new_inode(self, type):
        return InodeOps.Table_Inode(type)


    #PLEASE DO NOT MODIFY THIS
    #FLUSHES ALL THE BLOCKS OF INODES FROM GIVEN INDEX OF MAPPING ARRAY  
    def free_data_block(self, inode, index):
        for i in range(index, len(inode.blk_numbers)):
            interface.free_data_block(inode.blk_numbers[i])
            inode.blk_numbers[i] = -1



    def __write_to_filesystem_offset(self, inode, offset, data_array):
        flag = 0
        index = offset / config.BLOCK_SIZE
        for i in range(len(data_array)):
            if (inode.blk_numbers[index] != -1 and flag == 0):
                interface.update_data_block(inode.blk_numbers[index], data_array[i])
                index += 1
            else:
                flag = 1
                valid_block_number = interface.get_valid_data_block()
                interface.update_data_block(valid_block_number, data_array[i])
                inode.blk_numbers[index] = valid_block_number
                inode.size += 1
                index += 1


    #IMPLEMENTS WRITE FUNCTIONALITY
    def write(self, inode, offset, data):
        print("Writing data to the inode data block...")
        if inode.type == 1:
            print("\nInode is a directory: Operation not Permitted\n")
            return -1

        if inode.size == 0 and offset == 0:
            print("Initial write to the inode block")

            data_array = []
            for i in range(0, len(data), config.BLOCK_SIZE):
                data_array.append(data[i : i + config.BLOCK_SIZE])
            for i in range(len(data_array)):
                valid_block_number = interface.get_valid_data_block()
                interface.update_data_block(valid_block_number, data_array[i])
                inode.blk_numbers[i] = valid_block_number
                inode.size += 1 
        else:
            block_data = self.INODE_TO_BLOCK(inode, offset)
            file_index = offset / config.BLOCK_SIZE
            block_index = offset % config.BLOCK_SIZE

            if (block_data == '' or inode.blk_numbers[file_index] == -1):
                print("\noffset is out of bound: Operation not Permitted\n")
                return -1


            if block_index != 0:
                old_data = interface.BLOCK_NUMBER_TO_DATA_BLOCK(inode.blk_numbers[file_index])
                data = old_data[:block_index] + data

            data_array = []
            for i in range(0, len(data), config.BLOCK_SIZE):
                data_array.append(data[i : i + config.BLOCK_SIZE])

            self.__write_to_filesystem_offset(inode, offset, data_array)

        inode.time_accessed = str(datetime.datetime.now())[:19]
        inode.time_modified = str(datetime.datetime.now())[:19]



    #IMPLEMENTS THE READ FUNCTION 
    def read(self, inode, offset, length): 
        '''WRITE   YOUR CODE HERE '''
        print("Reading data from the inode data block")
        if inode.type == 1:
            print("\nInode is a directory: Operation not Permitted\n")
            return -1

    #IMPLEMENTS THE READ FUNCTION 
    def copy(self, inode): 
        '''WRITE   YOUR CODE HERE '''

    def status(self):
        print(MemoryInterface.status())

# temp debug function
    def printAttr(self, inode):
        print("printing blk numbers: ", inode.blk_numbers)
        print("time created: ", inode.time_created)
        print("time modified: ", inode.time_modified)
        print("time accessed: ", inode.time_accessed)
        print("inode size: ", inode.size)
        print("inode links: ", inode.links)

if __name__ == "__main__":
#    if len(sys.argv) < 3:
#        print("Usage: python HW1.py <string1> <string2>")
#        exit(0)
    test = InodeLayer()
    inodeObj = test.new_inode(0)
    dirInodeObj =  test.new_inode(1)
    test.printAttr(inodeObj)
    time.sleep(2)
    test.write(inodeObj, 0, "Hello World")
    test.printAttr(inodeObj)

    time.sleep(2)
    test.write(inodeObj, 12, "! This is great")
    test.printAttr(inodeObj)



 #   test.write(dirInodeObj, 100, "Hello")
    test.status()
