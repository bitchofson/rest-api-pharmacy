from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_ADRESS: str

    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str

    api_v1_prefix: str = '/api/v1'
    
    @property
    def database_url_asyncpg(self):
        # DSN{self.POSTGRES_HOST}
        # postgresql+psycopg://postgres:postgres@localhost:5432/dbname
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_ADRESS}:{self.DATABASE_PORT}/{self.POSTGRES_DB}'
    
    model_config = SettingsConfigDict(env_file='.env')

settings = Setting()