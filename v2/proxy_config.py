from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProxyConfig(BaseSettings):
    """
    Proxy configuration settings.
    """

    username: str
    password: str
    proxy: str

    model_config = SettingsConfigDict(
        env_file="proxy.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @field_validator("proxy")
    def validate_proxy(cls, value: str) -> str:
        """
        Validate the proxy format.
        """
        return f"http://{cls.username}:{cls.password}@gate.smartproxy.com:10001"
