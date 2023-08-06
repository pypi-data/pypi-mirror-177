from stochasticx.models.models import ModelType
from stochasticx.utils.file_utils import ModelUtils

class LocalModel:
    """Model class
    """
    
    def __init__(
        self,
        name: str,
        directory_path: str,
        model_type: str = ModelType.HUGGINGFACE
    ):
        """Initializer

        Args:
            name (str): model name
            directory_path (str): directory path where the model is located
            model_type (str, optional): model type. Defaults to ModelType.HUGGINGFACE.
        """
        assert isinstance(name, str), "The provided name {} is not valid".format(name)
        
        self.name = name
        self.directory_path = directory_path
        self.model_type = model_type
        self.model_id = None
        self.model_info = None
        self.is_uploaded = False
        
    def add(self):
        """Upload the model to the stochastic platform
        """
        
        model_id = ModelUtils.add_local_model(
            self.directory_path, 
            self.name, 
            self.model_type
        )
        
        self.set_id(model_id)
        self.is_uploaded = True
        
    def set_id(self, model_id: str):
        """Sets the model ID

        Args:
            model_id (str): new ID
        """
        self.model_id = model_id
        
    # def sync(self):
    #     """Syncs the model information with the stochastic platform
    #     """
        
    #     if self.model_id is not None:
    #         temp_model = Models.get_model(self.model_id)
    #         self.name = temp_model.name
    #         self.model_info = temp_model.model_info
    #         self.is_uploaded = True
    
    def get_id(self):
        """Gets the model ID

        Returns:
            str: the model ID
        """
        return self.model_id
    
    def get_model_info(self):
        """Gets the model information

        Returns:
            dict: model information
        """
        
        self.sync()
        
        return self.model_info
                
    def set_model_info(self, model_info):
        """Sets the model information

        Args:
            model_info (dict): model info
        """
        self.model_info = model_info
    
    def download(self, local_path: str):
        """Download the model for the Stochastic platform

        Args:
            local_path (str): path where the model will be saved
        """
        assert self.model_id is not None
        ModelUtils.download_model(self.model_id, local_path)
                    
    def __str__(self):
        """Convert the object to string

        Returns:
            str
        """
        return "Model ID: {} ; Name: {} ; Directory path: {} ; Model type: {} ; Uploaded: {}".format(
            self.model_id,
            self.name,
            self.directory_path,
            self.model_type,
            self.is_uploaded
        )
  