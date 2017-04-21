from sys import *
import os.path
import time
import struct

class PageLinksList():
	
	PRINT_INTERVAL = 30  #In milliseconds
	current_milli_time = lambda: int(round(time.time() * 1000))
	MAX_INT = 9223372036854775807
	@staticmethod
	def readSqlFile(file, titleToId, idToTitle):
		
		startTime = int(round(time.time() * 1000))
		rawlinks = [1]
		rawlinksLen = 0		
		inp = SqlReader(file, "pagelinks")
		
		try : 
		
			lastPrint = PageLinksList.current_milli_time() - PageLinksList.PRINT_INTERVAL
			while True :	
				multipleRows = inp.readInsertionTuples()
				
				if multipleRows is None:
					break
					
				for tuple in multipleRows :
					#Get tuple fields
					if len(tuple) != 4:
						raise Exception("Incorrect number of columns")
					srcId = tuple[0]
					namespace = tuple[1]
					destTitle = tuple[2]
					
					#Check data format
					if not isinstance(srcId, int):
						raise Exception("Source ID must be integer")
					if not isinstance(namespace, int):
						raise Exception("Namespace must be integer")
					if not isinstance(destTitle, int):
						raise Exception("Destination title must be integer")
					if int(namespace) == 0 and (srcId in idToTitle) and (destTitle in titleToId):
						continue  #Skip if not in main namespace or either page entry not found
					
					#Append to dynamic array
					if rawlinksLen == len(rawlinks):
						if rawlinksLen >= PageLinksList.MAX_INT / 2:
							raise Exception("Array size too large")
						#rawlinks = Arrays.copyOf(rawlinks, rawlinks.length * 2) --> inutil de le traduire 
					
					rawlinks[rawlinksLen] = titleToId[destTitle] << 32 | int(srcId)
					rawlinksLen+=1
					
				if PageLinksList.current_milli_time() - lastPrint >= PageLinksList.PRINT_INTERVAL :
					print("\rParsing {}: {} million entries stored".format(file, rawlinksLen / 1000000.0))
					lastPrint = PageLinksList.current_milli_time()
				
		except Exception:
			print("Error")
		
		print("\rParsing {}: {} million entries stored. Done ({} s)".format(file, rawlinksLen / 1000000.0, (PageLinksList.current_milli_time() - startTime) / 1000.0))
		
		return postprocessLinks(rawlinks, rawlinksLen)

	@staticmethod
	def postprocessLinks(rawlinks, rawlinksLen):
		
		print("Postprocessing links...")
		startTime = PageLinksList.current_milli_time()
		rawlinks.sort()
		
		links = [1]
		linksLen = 0
		
		for i in range(0, rawlinksLen) :
			dest = int(rawlinks[i] >> 32)
			j = i + 1
			while j < rawlinksLen and int((rawlinks[j] >> 32)) == dest :
				j+=1
				
			while linksLen + j - i + 2 >= len(links) :
				if linksLen >=  PageLinksList.MAX_INT / 2 :
					raise Exception("Array size too large")
				#links = Arrays.copyOf(links, links.length * 2) --> inutil de le traduire 
			
			linksLen+=1
			links[linksLen] = dest
			linksLen+=1
			links[linksLen] = j - i
			while i < j :
				linksLen+=1
				links[linksLen] = int(rawlinks[i])
				i+=1
		System.out.printf(" Done ({} s)".format((PageLinksList.current_milli_time()  - startTime) / 1000.0))
		return links
		
	@staticmethod
	def readRawFile(file) :
		startTime = PageLinksList.current_milli_time()
		result =[]
		inp = DataInputStream(open(file))
		try :
			lastPrint = PageLinksList.current_milli_time() - PageLinksList.PRINT_INTERVAL
			result = [inp.read_int()]
			for i in range(0, len(result)):
			
				result[i] = inp.read_int()
				
				if PageLinksList.current_milli_time() - lastPrint >= PageLinksList.PRINT_INTERVAL:
					print("\rReading {}: {} of {} million raw items...".format(file, i / 1000000.0, len(result) / 1000000.0))
					lastPrint = PageLinksList.current_milli_time()
				
			
			print("\rReading {}: {} of {} million raw items... Done ({} s)".format(file, len(result) / 1000000.0, len(result) / 1000000.0, (PageLinksList.current_milli_time() - startTime) / 1000.0))
				
		except Exception:
			print("Error")
		
		return result

		
	@staticmethod
	def writeRawFile(links, file):
		startTime = PageLinksList.current_milli_time()
		out = open(file)
		try :
			out.write(struct.pack("i",links.length))
			i = 0
			lastPrint = PageLinksList.current_milli_time() - PRINT_INTERVAL
			for link in links :
				out.write(struct.pack("i",links))
				i+=1
				
				if PageLinksList.current_milli_time()- lastPrint >= PageLinksList.PRINT_INTERVAL :
					print("\rWriting {}: {} of {} million raw items...".format(file, i / 1000000.0, len(links) / 1000000.0))
					lastPrint = PageLinksList.current_milli_time()
				
			
			print("\rWriting {}: {} of {} million raw items... Done ({} s)%n".format(file, i / 1000000.0, len(links) / 1000000.0, (PageLinksList.current_milli_time() - startTime) / 1000.0))
		except Exception:
			print("Error")
	
		

class DataInputStream:
    def __init__(self, stream):
        self.stream = stream

    def read_boolean(self):
        return struct.unpack('?', self.stream.read(1))[0]

    def read_byte(self):
        return struct.unpack('b', self.stream.read(1))[0]

    def read_unsigned_byte(self):
        return struct.unpack('B', self.stream.read(1))[0]

    def read_char(self):
        return chr(struct.unpack('>H', self.stream.read(2))[0])

    def read_double(self):
        return struct.unpack('>d', self.stream.read(8))[0]

    def read_float(self):
        return struct.unpack('>f', self.stream.read(4))[0]

    def read_short(self):
        return struct.unpack('>h', self.stream.read(2))[0]

    def read_unsigned_short(self):
        return struct.unpack('>H', self.stream.read(2))[0]

    def read_long(self):
        return struct.unpack('>q', self.stream.read(8))[0]

    def read_utf(self):
        utf_length = struct.unpack('>H', self.stream.read(2))[0]
        return self.stream.read(utf_length)

    def read_int(self):
        return struct.unpack('>i', self.stream.read(4))[0]