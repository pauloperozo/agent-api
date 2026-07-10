class DomainError(Exception):
    status_code = 400

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)
