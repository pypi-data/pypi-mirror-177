import os
import copy
import logging
import uuid
from typing import Text

from dataclasses import dataclass, fields


@dataclass(init=False)
class Settings:
    logger_name = "vector-search-api"

    # Pinecone
    pinecone_api_key: Text = str(uuid.uuid4())
    pinecone_environment: Text = "us-west1-gcp"
    pinecone_index_name: Text = "pinecone-index"
    pinecone_namespace: Text = ""

    def __init__(self, **kwargs):
        environ = copy.deepcopy(dict(os.environ))
        environ.update(**kwargs)

        case_insensitive_environ = {}
        for env, value in environ.items():
            case_insensitive_environ[env.casefold()] = value

        environ.update(case_insensitive_environ)

        for self_field in fields(self):
            if self_field.name.casefold() in environ:
                setattr(
                    self,
                    self_field.name,
                    self_field.type(environ[self_field.name.casefold()]),
                )


settings = Settings()
logger = logging.getLogger(settings.logger_name)
