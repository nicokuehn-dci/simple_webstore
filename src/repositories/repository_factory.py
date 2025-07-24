"""
Repository Factory - Choose between JSON and CSV storage
"""
from .json_repository import JSONRepository
from .csv_repository import CSVRepository


class RepositoryFactory:
    """Factory for creating repository instances"""
    
    @staticmethod
    def create_repository(repo_type: str = "json", data_dir: str = "data"):
        """Create repository instance
        
        Args:
            repo_type: "json" or "csv"
            data_dir: Directory for data files
            
        Returns:
            Repository instance
        """
        if repo_type.lower() == "csv":
            return CSVRepository(data_dir)
        elif repo_type.lower() == "json":
            return JSONRepository(data_dir)
        else:
            raise ValueError(f"Unsupported repository type: {repo_type}")
    
    @staticmethod
    def get_available_types():
        """Get list of available repository types"""
        return ["json", "csv"]
