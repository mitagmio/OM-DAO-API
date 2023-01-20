from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    db_url: PostgresDsn = 'postgresql+psycopg2://omdao:omdao@db:5432/omdao'

    infura_url: str = 'https://mainnet.infura.io/v3/'
    infura_api_key: str = '8d45d8cbaf43475598efac94ece379b9'

    contract_address: str = '0x9a4d39F46044400Aa48Ab528f8EC3DD3B793f885'
    base_referal_code: str = '0x6261736500000000000000000000000000000000000000000000000000000000'

    start_block_number: int = 16242482


settings = Settings()
