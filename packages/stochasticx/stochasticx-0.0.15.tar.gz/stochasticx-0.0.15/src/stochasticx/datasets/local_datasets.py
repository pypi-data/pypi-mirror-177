
from stochasticx.datasets.datasets import DatasetType, Datasets
from stochasticx.utils.file_utils import DatasetUtils


class LocalDataset:
    """Dataset class
    """
    
    def __init__(
        self,
        name: str,
        directory_path: str,
        dataset_type: str = DatasetType.HUGGINGFACE
    ):
        """Initializer

        Args:
            name (str): dataset name
            directory_path (str): directory in which your dataset is stored
            dataset_type (str, optional): dataset type. Defaults to DatasetType.HUGGINGFACE.
        """
        assert isinstance(name, str), "The provided name {} is not valid".format(name)
        self.name = name
        self.directory_path = directory_path
        self.dataset_type = dataset_type
        self.column_names = []
        self.dataset_id = None
        self.dataset_info = None
        self.is_uploaded = False
        
    def add(self):
        """Uploads the dataset to the Stochastic platform
        """
        
        assert self.directory_path is not None
        
        dataset_id = DatasetUtils.add_local_dataset(
            self.directory_path, 
            self.name, 
            self.dataset_type
        )
        
        self.set_id(dataset_id)
        self.is_uploaded = True
        
    def set_id(self, dataset_id: str):
        """Set the ID of the dataset

        Args:
            dataset_id (str): the new ID
        """
        self.dataset_id = dataset_id
        
    def get_id(self):
        """Returns the ID of the dataset

        Returns:
            str: the ID
        """
        return self.dataset_id
    
    def sync(self):
        """Synchronize the current dataset with the cloud
        """
        
        if self.dataset_id is not None:
            temp_ds = Datasets.get_dataset(self.dataset_id)
            self.dataset_info = temp_ds.dataset_info
            self.name = temp_ds.name
    
    def get_dataset_info(self):
        """Gets the dataset information

        Returns:
            dict: dataset information
        """
        
        self.sync()
        
        return self.dataset_info
                
    def set_dataset_info(self, dataset_info):
        """Sets the dataset information

        Args:
            dataset_info (dict): dataset information
        """
        self.dataset_info = dataset_info
        
    def get_column_names(self):
        """Get column names of the dataset

        Returns:
            List[str]: the column names
        """
        if self.dataset_id is not None:
            temp_ds = Datasets.get_dataset(self.dataset_id)
            self.column_names = temp_ds.column_names
            
        return self.column_names
        
    def set_column_names(self, column_names):
        """Set the column names of the dataset

        Args:
            column_names (List[str]): new column names
        """
        self.column_names = column_names
    
    def download(self, local_path: str):
        """Downloads the dataset

        Args:
            local_path (str): local path where the dataset is saved
        """
        assert self.dataset_id is not None
        DatasetUtils.download_dataset(self.dataset_id, local_path)
                    
    def __str__(self):
        """Method to convert the object to string

        Returns:
            str: string
        """
        return "ID: {} ; Dataset name: {} ; Directory path: {} ; Dataset type: {} ; Uploaded: {}".format(
            self.dataset_id,
            self.name,
            self.directory_path,
            self.dataset_type,
            self.is_uploaded
        )
