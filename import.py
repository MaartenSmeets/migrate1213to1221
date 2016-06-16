import wlstModule
import sys

from com.bea.wli.sb.management.configuration import SessionManagementMBean
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.config import Ref
from com.bea.wli.config.customization import Customization
from java.io import FileInputStream 
from java.util import HashMap
from java.util import ArrayList
from java.util import HashSet

import sys

#=======================================================================================
# Entry function to deploy project configuration and resources
#        into a ALSB domain
# use from Bamboo in script task:
# export JAVA_HOME=/usr/java/jdk1.7.0_71
#/home/oracle/Oracle/Middleware/Oracle_Home/soa/common/bin/wlst.sh build/import.py ${bamboo.sca_server_deploy_ont_url} ${bamboo.sca_deploy_ont_username} ${bamboo.sca_deploy_ont_password}
#
#=======================================================================================

def importToALSBDomain():
	try:
		# Declare Variables
		sessionMBean = None
		alsbConfigurationMBean = None
		
		
		# Connect to Server
		print 'Connecting to server: ', adminUrl
		connectToServer(connectMethod)

		print 'Starting import of:', importJar, "on ALSB Admin Server:", adminUrl

		# Read import jar file
		print 'Read import jar file'
		theBytes = readBinaryFile(importJar)
		print 'Import file read successfully', importJar

		# Create unique session name	
		print 'Creating unique session name'
		sessionName = createSessionName()
		print 'Created session name :', sessionName

		# Create and start session
		print 'Creating SessionMBean'
		sessionMBean = getSessionMBean(sessionName)
		print 'SessionMBean started new session'

		# obtain the ALSBConfigurationMBean instance that operates
		# on the session that has just been created. Notice that
		# the name of the mbean contains the session name.
		print 'Create ALSBConfiguration'
		alsbConfigurationMBean = findService(String(ALSBConfigurationMBean.NAME + ".").concat(sessionName), ALSBConfigurationMBean.TYPE)
		print "ALSBConfiguration MBean found", alsbConfigurationMBean

		# Perform updates or read operations in the session using alsbSession

		# Upload Jar File
		print 'Uploading Jar file'
		alsbConfigurationMBean.uploadJarFile(theBytes)
		print 'Jar Uploaded'

		print 'ALSB Project will now get imported'
		alsbJarInfo = alsbConfigurationMBean.getImportJarInfo()

		alsbImportPlan = alsbJarInfo.getDefaultImportPlan()

		#alsbImportPlan.setPassphrase(passphrase)

		operationMap=HashMap()

		operationMap = alsbImportPlan.getOperations()

		print 'Default importPlan'
		printOpMap(operationMap)

		alsbImportPlan.setPreserveExistingEnvValues(preserveExistingEnvValues)
		alsbImportPlan.setPreserveExistingOperationalValues(preserveExistingOperationalValues)

		print 'Modified importPlan'
		printOpMap(operationMap)
		importResult = alsbConfigurationMBean.importUploaded(alsbImportPlan)

		printDiagMap(importResult.getImportDiagnostics())

		if importResult.getFailed().isEmpty() == false:
			print 'One or more resources could not be imported properly'
			raise

		

		#customize if a customization file is specified
		#affects only the created resources
		if customFile != None :
			print 'Loading customization File', customFile
			iStream = FileInputStream(customFile)
			customizationList = Customization.fromXML(iStream)
			alsbConfigurationMBean.customize(customizationList)

		sessionMBean.activateSession(sessionName, "ALSBImport Operation Completed Successfully")

		print "Deployment of : " + importJar + " successful"
	except:
		print "Unexpected error:", sys.exc_info()[0]
		if sessionMBean != None:
			sessionMBean.discardSession(sessionName)
		raise


#=======================================================================================
# Utility function to print the list of operations
#=======================================================================================
def printOpMap(map):
    set = map.entrySet()
    for entry in set:
        op = entry.getValue()
        print op.getOperation(),
        ref = entry.getKey()
        print ref
    print

#=======================================================================================
# Utility function to print the diagnostics
#=======================================================================================
def printDiagMap(map):
    set = map.entrySet()
    for entry in set:
        diag = entry.getValue().toString()
        print diag
    print

#=======================================================================================
# Connect to the Admin Server
#=======================================================================================

def connectToServer(connnectMethod):
    if connectMethod == "boot":
       connect(url=adminUrl, adminServerName=adminServer)
    else:
       connect(username, password, adminUrl)
       
    domainRuntime()

#=======================================================================================
# Utility function to read a binary file
#=======================================================================================
def readBinaryFile(fileName):
    file = open(fileName, 'rb')
    bytes = file.read()
    return bytes

#=======================================================================================
# Utility function to create an arbitrary session name
#=======================================================================================
def createSessionName():
    sessionName = String("ALSBImportScript-"+Long(System.currentTimeMillis()).toString())
    return sessionName

#=======================================================================================
# Utility function to load a session MBeans
#=======================================================================================
def getSessionMBean(sessionName):
    # obtain session management mbean to create a session.
    # This mbean instance can be used more than once to
    # create/discard/commit many sessions
    sessionMBean = findService(SessionManagementMBean.NAME,SessionManagementMBean.TYPE)

    # create a session
    sessionMBean.createSession(sessionName)

    return sessionMBean



# IMPORT script init
try:
    # import the service bus configuration
    username=sys.argv[1]  
    password=sys.argv[2]
    adminUrl=sys.argv[3]
    importJar=sys.argv[4] 
    customFile=sys.argv[5] 
    preserveEnv=sys.argv[6]
    preserveOperational=sys.argv[7]

    if preserveEnv == "preserveExistingEnvValues":
        preserveExistingEnvValues = true
        print "preserve environment values"
    else:
        preserveExistingEnvValues = false
        print "do not preserve environment values"	

    if preserveOperational == "preserveExistingOperationalValues":
        preserveExistingOperationalValues = true
        print "preserve operational values"
    else:
        preserveExistingOperationalValues = false
        print "do not preserve operational values"	

    connectMethod='normal'
    print "input param 1 user: ", username
    print "input param 2: pw", password
    print "input param 3: adminurl", adminUrl
    print "input param 4: jar", importJar
    print "input param 5: customfile", customFile 
    print "input param 6: preserve environment values (0 is false,1 is true)", preserveExistingEnvValues
    print "input param 7: preserve operational values (0 is false,1 is true)", preserveExistingOperationalValues 	
    importToALSBDomain()

except:
    print "Unexpected error: ", sys.exc_info()[0]
    dumpStack()
    exit(exitcode=1)
