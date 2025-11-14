class BaseScraper:
    def __init__(self):
        pass

    def fetch(self):
        raise NotImplementedError("fetch() must be implemented in child classes")
