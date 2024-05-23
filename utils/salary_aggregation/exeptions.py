class ValidationException(Exception):
    """
    в details передавать поле в котором ошибка в качесвте ключа и текст ошибки в качесвте значения
    """

    def __init__(self, message: str | None, details: dict):
        self.message = message or 'Some error'
        self.details = details
