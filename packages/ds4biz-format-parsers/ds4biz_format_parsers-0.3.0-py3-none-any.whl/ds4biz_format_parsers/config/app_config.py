from ds4biz_commons.utils.config_utils import EnvConfig
env=EnvConfig()

TEXTRACT_URL=env.TEXTRACT_URL or "http://localhost:8080/ds4biz/textract/0.2/"