import os
from types import ModuleType

from dotenv import load_dotenv

load_dotenv()


class MetaEnv(type):
    @classmethod
    def _get_env_vars(mcs, var_name):  # type: ignore
        value = os.getenv(var_name)
        if value is None:
            raise ValueError(f"{var_name} is not defined in .env")
        return value

    @property
    def PGHOST(cls):
        return cls._get_env_vars("PGHOST")

    @property
    def PGPORT(cls):
        return cls._get_env_vars("PGPORT")

    @property
    def PGDATABASE(cls):
        return cls._get_env_vars("PGDATABASE")

    @property
    def PGUSER(cls):
        return cls._get_env_vars("PGUSER")

    @property
    def PGPASSWORD(cls):
        return cls._get_env_vars("PGPASSWORD")

    @property
    def POOL_SIZE(cls):
        return cls._get_env_vars("POOL_SIZE")

    @property
    def SECRET_KEY(cls):
        return cls._get_env_vars("SECRET_KEY")

    @property
    def ALGORITHM(cls):
        return cls._get_env_vars("ALGORITHM")

    @property
    def DATABASE_URL(cls):
        return cls._get_env_vars("DATABASE_URL")

    @property
    def SERVER_MODE(cls):
        return cls._get_env_vars("SERVER_MODE")


class ENV(ModuleType, metaclass=MetaEnv):
    pass


__all__ = ["ENV"]
