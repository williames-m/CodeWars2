from src.exception.base_funcionario_error import DataBaseError

class NotFoundError(DataBaseError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
