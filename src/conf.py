# Standard Library
from typing import Optional

# Third Party Library
from pydantic import (
	BaseSettings,
	PostgresDsn,
)


class Settings(BaseSettings):
	project: str = 'test-task'

	postgres_host: str
	postgres_port: str
	postgres_db: str
	postgres_user: str
	postgres_password: str

	log_dir: str = 'logs'
	log_filename: str = 'logs.log'
	log_level: str = 'INFO'
	log_rotation: int = 2  # 2 MB
	log_retention: int = 3  # 3 days

	class Config:
		env_file = '.env'
		env_nested_delimiter = '__'

	@property
	def database_dsn(
		self
	) -> str:
		return PostgresDsn.build(
			scheme='postgresql+asyncpg',
			user=self.postgres_user,
			password=self.postgres_password,
			host=self.postgres_host,
			port=self.postgres_port,
			path=f'/{self.postgres_db}',
		)


settings = Settings()
