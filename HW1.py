import BlockLayer, sys, config, MemoryInterface

MemoryInterface.Initialize_My_FileSystem()
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

	#WRITE TO FILESYSTEM
	def __write_to_filesystem(self, data_array):
		for i in range(len(data_array)):
			valid_block_number = interface.get_valid_data_block()
			interface.update_data_block(valid_block_number, data_array[i])
			self.map.append(valid_block_number)

	def __write_to_filesystem_offset(self, block_offset, data_array):
		flag = 0
		#print "block_offset: ", block_offset
		#print "len(self.map): ", len(self.map)
		for i in range(len(data_array)):
			if (block_offset < len(self.map) and flag == 0):
				interface.update_data_block(self.map[block_offset], data_array[i])
				block_offset += 1
			else:
				flag = 1
				valid_block_number = interface.get_valid_data_block()
				interface.update_data_block(valid_block_number, data_array[i])
				self.map.append(valid_block_number)

	#STATUS FUNCTION TO CHECK THE STATUS OF THE DATA BLOCKS IN THE MEMORY
	def status(self):
		print(MemoryInterface.status())

	# WRITE TO OFFSET (refer to assignment doc)
	def write_to_offset(self,offset,string):
		data_array = []
		#check valid offset value
		block_offset = offset / config.BLOCK_SIZE
		block_index = offset % config.BLOCK_SIZE
		if (block_offset >= len(self.map)):
			print "error, offset landed on illegal block number.\nOperation didn't go through"
			return
		if block_index != 0:
			old_data = interface.BLOCK_NUMBER_TO_DATA_BLOCK(self.map[block_offset])
			string = old_data[:block_index] + string

		for i in range(0, len(string), config.BLOCK_SIZE):
			data_array.append(string[i : i + config.BLOCK_SIZE])
		self.__write_to_filesystem_offset(block_offset, data_array)

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: python HW1.py <string1> <string2>")
		exit(0)
	test = Operations()
	test.write(sys.argv[1])
	test.read()
	test.status()
	test.write_to_offset(int(sys.argv[3]),sys.argv[2])
	test.read()
	# last call
	test.status()

