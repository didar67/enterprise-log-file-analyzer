"""
Config Loader Module
Loads and validates YAML configuration using Pydantic models.
This ensures type safety and prevents runtime errors due to config changes
"""
import yaml
from pydantic import BaseModel, Field
from typing import Literal
from pathlib import Path

class AppConfig(BaseModel):
    """
    Configuration schema for application-specific settings
    """
    log_file_path: Path
    dry_run: bool = Field(default=False)
    async_chunk_size: int = Field(default=1024, gt=0)  # enforce positive chunk size
    
class LoggingConfig(BaseModel):
    """
    Configuration schema for logging settings
    """
    log_file: Path
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    max_bytes: int = Field(gt=0)  # positive integer enforced
    backup_count: int = Field(ge=0)   # zero or positive
    
class Config(BaseModel):
    """
    Main configuration schema for the app
    """
    app: AppConfig
    logging: LoggingConfig
    
def load_config(file_path: Path) -> Config:
    """
    Load and validate YAML configuration file
    """
    # Reading YAML safely to avoid code execution risks
    with open (file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    # Pydantic validation ensures strict type and value checks
    return Config(**data)