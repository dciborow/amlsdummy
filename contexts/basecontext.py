import platform
from scripts.azure_utils import setContext
from azureml.core.image import ContainerImage
from scripts.azure_utils import *

class BaseContext:

    '''
        Contains base context items
    '''
    def __init__(self, programArgs, userAuthorization):
        self.programArguments = programArgs
        self.authentication = userAuthorization
        self.platform = platform.system().lower()
        self.workspace = None
        self.experiment = None
        self.model = None

        if not self.authentication:
            raise Exception("Authentication object missing")

        '''
            Change the context to the provided subscription id
            This expects that an az login has already occured with a user
            that has the correct credentials.
        '''
        setContext(self.programArguments.subid)


    def generateWorkspace(self):
        '''
            Gets an existing workspace (by name) or creates a new one
        '''
        
        self.workspace = getWorkspace(
            self.authentication, 
            self.programArguments.subid, 
            self.programArguments.resourceGroup,
            self.programArguments.workspace,
            self.programArguments.region
            )

        if not self.workspace:
            raise Exception("Workspace Creation Failed")

    def generateExperiment(self):
        '''
            Get an existing experiment by name, or create new
        '''
        self.experiment = getExperiment(self.workspace, self.programArguments.experiment)

        if not self.experiment:
            raise Exception("Experiment Creation Failed")


