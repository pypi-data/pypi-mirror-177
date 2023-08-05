class CurrencyException(Exception): ...

class CurrencyInvalidDivision(CurrencyException, TypeError):
    def __init__(self, *args: object) -> None: ...

class CurrencyInvalidFormat(CurrencyException, ValueError):
    def __init__(self, *args: object) -> None: ...

class CurrencyInvalidMultiplication(CurrencyException, TypeError):
    def __init__(self, *args: object) -> None: ...

class CurrencyInvalidOperation(CurrencyException, TypeError):
    def __init__(self, *args: object) -> None: ...

class CurrencyMismatchException(CurrencyException, TypeError):
    def __init__(self, *args: object) -> None: ...

class CurrencyTypeException(CurrencyException, TypeError):
    def __init__(self, *args: object) -> None: ...
