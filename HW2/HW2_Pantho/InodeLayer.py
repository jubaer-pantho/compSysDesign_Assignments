import datetime, sys, time, config, BlockLayer, InodeOps, MemoryInterface


MemoryInterface.Initialize_My_FileSystem()
#HANDLE OF BLOCK LAYER
interface = BlockLayer.BlockLayer()

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

    # helper function to write data to the blocks
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
                if (index >= len(inode.blk_numbers)):
                    print("\nWrite size too big: Operation not Permitted\n")
                    return
                inode.blk_numbers[index] = valid_block_number
                inode.size += 1
                index += 1


    #IMPLEMENTS WRITE FUNCTIONALITY
    def write(self, inode, offset, data):
        if inode.type == 1:
            print("\nInode is a directory: Operation not Permitted\n")
            return -1

        # the if condition will be only executed if the file size is 0
        # for the first time
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
        return inode


    #IMPLEMENTS THE READ FUNCTION 
    def read(self, inode, offset, length): 
        '''WRITE   YOUR CODE HERE '''
        if inode.type == 1:
            print("\nInode is a directory: Operation not Permitted\n")
            return -1

        block_data = self.INODE_TO_BLOCK(inode, offset)
        file_index = offset / config.BLOCK_SIZE
        block_index = offset % config.BLOCK_SIZE

        if (block_data == '' or inode.blk_numbers[file_index] == -1):
                print("\noffset is out of bound: Operation not Permitted\n")
                return -1

        # reading the first block with offset
        data_read = interface.BLOCK_NUMBER_TO_DATA_BLOCK(inode.blk_numbers[file_index])
        file_index += 1
        data_array = []

        x = config.BLOCK_SIZE - block_index

        if x > length:
            x = block_index + length
            length = 0
        else:
            length = length - x
            x = config.BLOCK_SIZE

        data_array.append(data_read[block_index:x])

        # reading the rest of the blocks
        while(length):
            file_index += 1
            x = length if config.BLOCK_SIZE > length else config.BLOCK_SIZE
            
            data_read = interface.BLOCK_NUMBER_TO_DATA_BLOCK(inode.blk_numbers[file_index])
            data_array.append(data_read[:x])
            length -= x

        inode.time_accessed = str(datetime.datetime.now())[:19]
        return inode, "".join(data_array)


    #IMPLEMENTS THE READ FUNCTION 
    def copy(self, inode): 
        newInodeObj = test.new_inode(0)
        # copying blocks to make a deep copy
        for i in range(0, len(inode.blk_numbers)):
            if (inode.blk_numbers[i] == -1):
                break
            data_read = interface.BLOCK_NUMBER_TO_DATA_BLOCK(inode.blk_numbers[i])
            valid_block_number = interface.get_valid_data_block()
            interface.update_data_block(valid_block_number, data_read)
            newInodeObj.blk_numbers[i] = valid_block_number

        newInodeObj.time_modified = str(datetime.datetime.now())[:19]
        newInodeObj.time_accessed = inode.time_accessed = str(datetime.datetime.now())[:19]
        newInodeObj.size = inode.size
        newInodeObj.links = inode.links

        return newInodeObj


    def status(self):
        print(MemoryInterface.status())

# debug print function
    def printAttr(self, inode):
        print("\nprinting blk numbers: ", inode.blk_numbers)
        print("time created: ", inode.time_created)
        print("time modified: ", inode.time_modified)
        print("time accessed: ", inode.time_accessed)
        print("inode size: ", inode.size)
        print("inode links: ", inode.links)

if __name__ == "__main__":

    test = InodeLayer()
    inodeObj = test.new_inode(0)
    dirInodeObj =  test.new_inode(1)
    # first write
    print("\nWriting data to the inode data block...")
    inodeObj = test.write(inodeObj, 0, "Hello World")

    time.sleep(1)
    # second write
    print("\nWriting data to the inode data block...")
    inodeObj = test.write(inodeObj, 12, "! This is great")
    test.printAttr(inodeObj)

    # read operation
    print("\nReading data to the inode data block...")
    _ , data_read = test.read(inodeObj, 0, 16)
    print ("read result : " + data_read)

    print("\ncopying data to the new file (deep copy)...")
    copyObj = test.copy(inodeObj)

    test.printAttr(copyObj)

    test.status()
