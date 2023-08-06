from ds4biz_commons.utils.requests_utils import URLRequest


class RESTDS4BizTextract:  # Lo cambiamo in RESTDS4BizTextract ?

    def __init__(self, url):
        self.u = URLRequest(url)

    def extract(self, filename: str) -> str:
        with open(filename, "rb") as f:
            r = self.u.extract.post(files=dict(file=f))
        return r

# Perchè? usare requests raise_for_status e catchare l'eccezione e risollevarla
