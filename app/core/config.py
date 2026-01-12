from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	# App
	name: str = 'Legalian - Take Home - Graph API'

	# Debug
	debug_mode: bool = False

	# Database
	db_host: str = 'localhost'
	db_port: int = 3306
	db_user: str = 'root'
	db_password: str = '1234'
	db_name: str = 'graph_db'

	@property
	def database_url(self) -> str:
		return (
			f'mysql+pymysql://{self.db_user}:'
			f'{self.db_password}@'
			f'{self.db_host}:{self.db_port}/'
			f'{self.db_name}'
		)

	model_config = SettingsConfigDict(env_prefix='APP_', case_sensitive=False)


settings = Settings()
