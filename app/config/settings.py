from pydantic import BaseSettings, PostgresDsn
import os
import dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Load env variables from file
dotenv_file = BASE_DIR / ".env"
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

class Settings(BaseSettings):
    db_url: PostgresDsn = os.getenv("POSTGRESDSN", default='')

    infura_url: str = 'https://mainnet.infura.io/v3/'
    # infura_api_key: str = '8d45d8cbaf43475598efac94ece379b9'
    infura_api_key: str = os.getenv("INFURA_API_KEY", default='')

    contract_address: str = '0x9a4d39F46044400Aa48Ab528f8EC3DD3B793f885'

    start_block_number: int = 16240000
    batch_size: int = 10000


settings = Settings()
