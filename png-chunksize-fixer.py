#!/usr/bin/env python

'''

MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import argparse
import collections

class PngFixer:

	parser = None
	config = None

	PNG_HEADERS_CRITICAL = [b'IHDR', b'PLTE', b'IDAT', b'IEND']
	PNG_HEADERS_ANCILLARY = [b'bKGD', b'cHRM', b'dSIG', b'eXIf', b'gAMA', b'hIST', 
		b'iCCP', b'iTXt', b'pHYs', b'sBIT', b'sPLT', b'sRGB', b'sTER', b'tEXt', b'tIME', 
		b'tRNS', b'zTXt']
	PNG_HEADERS = PNG_HEADERS_CRITICAL + PNG_HEADERS_ANCILLARY

	def __init__(self):
		self.parse_args()
		self.fix_chunks(self.config['input'], self.config['output'])

	def parse_args(self):
		self.parser = argparse.ArgumentParser(description = "Fix PNG Critical Chunk Sizes", usage='./%(prog)s -i input.png [-o output.png]')
		self.parser.add_argument('-i', '--input-file', dest='input', required=True, help='Input file name')
		self.parser.add_argument('-o', '--output-file', dest='output', default='output.png', help="Output file name (Default 'output.png')")
		self.config = vars(self.parser.parse_args())

	def fix_chunks(self, infile, outfile):
		file_not_exists = False

		try:
			with open(infile, 'rb', buffering=0) as f:
				all_bytes = f.readall() # All bytes from the input file read
				new_bytes = all_bytes # Bytes to output to output file

				error_msg, errorred = self.check_errors(all_bytes)
				if errorred:
					print(error_msg)
					return

				''' Find each header, fix their chunk sizes '''
				for critical_header in self.PNG_HEADERS_CRITICAL:
					if critical_header == b'IEND':
						break

					start_index = all_bytes.find(critical_header)
					end_index = 99999999999999999999
					chunksize = 0

					h = b'notfound'

					for header in self.PNG_HEADERS:
						temp_index = all_bytes.find(header, start_index)

						# Find the next chunk that occurs immediately after the current critical header
						if temp_index < end_index and temp_index != -1 and header != critical_header:
							end_index = temp_index

							'''
							The 4 bytes before the next chunk is the next chunk's size
							The 4 bytes before that is the current chunk's CRC
							Therefore we go back 8 bytes
							'''
							end_index -= 8
							chunksize = end_index - (start_index+4)

					# Read the current chunksize specified in the file into a variable
					existing_chunksize = int.from_bytes(all_bytes[start_index-4:start_index], 'big')

					'''
					If the calculated chunksize does not match the file's specified chunk size,
					then we need to change it
					'''
					if existing_chunksize != chunksize:
						print(existing_chunksize)
						new_bytes = new_bytes[0:start_index-4] # Read up to the current chunksize
						new_bytes += chunksize.to_bytes(4, 'big') # Replace with our calculated chunksize
						new_bytes += all_bytes[start_index:] # Concat the rest of the bytes

				with open(outfile, 'wb', buffering=0) as o:
					o.write(new_bytes)
		except Exception as e: 
			file_not_exists = True
			print("ERROR: {0}".format(e))


		print()

		if not file_not_exists:
			print("Done! Output to file " + outfile)

	'''
	Checks for errors in the PNG file
	'''
	def check_errors(self, all_bytes):
		errorred = False
		error_msg = b''

		'''
		Checks to make sure the file is actually a PNG file to begin with
		'''
		if b'PNG' not in all_bytes:
			errorred = True
			error_msg += b"ERROR: Not a PNG file  "

		if errorred: return (error_msg, errorred)

		'''
		Checks to make sure none of the critical chunks are missing
		'''
		error_msg += b"ERROR: Missing critical chunks "
		for header in self.PNG_HEADERS_CRITICAL:
			if header not in all_bytes:
				errorred = True
				error_msg += header + b", "

		return (error_msg[:-2], errorred)
				


if __name__ == '__main__':
	PngFixer()