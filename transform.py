import sys
 
from java.io import FileReader, PrintWriter
from java.lang import System
from javax.xml.transform import TransformerFactory, Transformer
from javax.xml.transform.stream import StreamSource, StreamResult

def transform(source, stylesheet, result, parameters):
    transformer = TransformerFactory.newInstance().newTransformer(stylesheet)
    for (p, v) in parameters: transformer.setParameter(p, v)
    transformer.transform(source, result)
 
args = sys.argv[1:]
parameters = []
while args and args[0].startswith('-'):
   try:
       i = args[0].index('=')
   except ValueError:
       parameters.append((args[0], ""))
   else:
       parameters.append((args[0][1:i], args[0][i+1:]))
   args = args[1:]
   
if len(args) == 1: source = StreamSource(System.in)
elif len(args) >= 2: source = StreamSource(FileReader(args[1]))
else: raise "Usage: <jython|wlst> transform.py -<parameter>=<value> <stylesheetfile> [inputfile] [outputfile]"

if len(args) == 3: output = args[2]
else: output = ""
 
stylesheet = StreamSource(FileReader(args[0]))
if len(output) == 0:
	result = StreamResult(PrintWriter(System.out))
else:
	result = StreamResult(FileWriter(File(output)))
 
transform(source, stylesheet, result, parameters)
 
stylesheet.reader.close()
source.reader and source.reader.close()
result.writer.close()