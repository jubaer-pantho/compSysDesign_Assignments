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
            print("Inode is a directory: Operation not Permitted")
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
                print("offset is out of bound: Operation not Permitted")
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
        if inode.type == 1:
            print("Inode is a directory: Operation not Permitted")
            return -1

        block_data = self.INODE_TO_BLOCK(inode, offset)
        file_index = offset / config.BLOCK_SIZE
        block_index = offset % config.BLOCK_SIZE

        if (block_data == '' or inode.blk_numbers[file_index] == -1):
                print("offset is out of bound: Operation not Permitted")
                return -1

        # reading the first block with offset
        data_read = interface.BLOCK_NUMBER_TO_DATA_BLOCK(inode.blk_numbers[file_index]) 
        data_array = []

        x = config.BLOCK_SIZE - block_index

        if x > length:
            x = block_index + length
            length = 0
        else:
            length = length - x
            x = config.BLOCK_SIZE

        data_array.append(data_read[block_index:x])

        #reading the rest of the blocks
        while(length):
            file_index += 1
            x = length if config.BLOCK_SIZE > length else config.BLOCK_SIZE
            if (inode.blk_numbers[file_index] == -1):
                print("Length goes beyond allocated blocks")
                return -1
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
        print("printing blk numbers: ", inode.blk_numbers)
        print("time created: ", inode.time_created)
        print("time modified: ", inode.time_modified)
        print("time accessed: ", inode.time_accessed)
        print("inode size: ", inode.size)
        print("inode links: ", inode.links)

if __name__ == "__main__":

    test = InodeLayer()
    inodeObj = test.new_inode(0)

    print ("\nTEST 0:\n")
    dirInodeObj =  test.new_inode(1)
    ret = test.read(dirInodeObj, 0, 8)
    if (ret == -1):
        print("read  attempt to inode that is not file: PASSED")


    print ("\nTEST 1:\n")
    ret = test.write(dirInodeObj, 0, "")
    ret = test.read(dirInodeObj, 0, 8)
    if (ret == -1):
        print("write attempt to inode that is not file: PASSED")

     
    print ("\nTEST 2:\n")
    inodeObj = test.write(inodeObj, 0, "01234567") 
    _ , data_read = test.read(inodeObj, 0, 8)
    print ("write initial string to file - result: " + data_read)


    time.sleep(1)
    print ("\nTEST 3:\n")
    copyObj = test.copy(inodeObj)
    _ , data_read = test.read(copyObj, 0, 8)
    print ("copy of file - result: " + data_read)


    print ("\nTEST 4:\n")
    _ , data_read = test.read(inodeObj, 2, 2)
    print ("read file at an offset - result: " + data_read)


    print ("\nTEST 5:\n")
    inodeObj = test.write(inodeObj, 1, "writehere")
    _ , data_read = test.read(inodeObj, 0, 10)
    print ("writing to middle of file - result: " + data_read)

    print ("\nTEST 6:\n")
    ret = test.write(inodeObj, 12, "beyond") 
    ret = test.read(inodeObj, 0, 16)
    if (ret == -1):
        print("write attempt beyond file size: PASSED")
    
    print ("\nTEST 7:\n")
    ret = test.read(inodeObj, offset=12, length=3)
    if (ret == -1):
        print("read attempt beyond file size: PASSED")

    print ("\nTEST 8:\n")
    inodeObj = test.write(inode=inodeObj, offset=0, data="reset\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    _ , data_read = test.read(inodeObj, 0, 5)
    print ("write reset to the file at 0 - result: " + data_read)

    print ("\nTEST 9:\n")
    inodeObj = test.write(inode=inodeObj, offset=5, data=" append")
    _ , data_read = test.read(inode=inodeObj, offset=0, length=12)
    print ("write append to end of file - result: " + data_read)

    print ("\nTEST 10:\n")
    inodeObj = test.write(inode=inodeObj, offset=0, data="0000    0002    0004    0006    ")
    _ , data_read = test.read(inode=inodeObj, offset=0, length=16)
    print ("(truncate) System Calls in Test - result: " + data_read)

    print("\n\n")

    test.status()
