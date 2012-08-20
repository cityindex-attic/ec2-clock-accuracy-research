#!/usr/bin/python
import argparse
import base64
from StringIO import StringIO
from gzip import GzipFile

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Decode a base64 encoded gzipped file')
parser.add_argument("source", help="The source content (or filename for --encode")
parser.add_argument("-e", "--encode", action='store_true', help="Gzip then base64 encode file")

args = parser.parse_args()

output = ""
if args.encode:
	out = StringIO()
	f = GzipFile(fileobj=out, mode='w')
	f.write(open(args.source, 'r').read())
	f.close()
	output = base64.b64encode(out.getvalue())
else:
	base64_content = args.source
	gzipped_content = base64.b64decode(base64_content)
	output = GzipFile('', 'r', 0, StringIO(gzipped_content)).read()

print output

