import logging


class DataHandler:
    __slots__ = ["logger", "fh", "filename"]

    def __init__(self, filename: str = "data/data.txt"):
        self.filename: str = filename
        logging.info(f"File Handler created on File: {self.filename}")
        self.logger = logging.getLogger("my_logger")
        self.logger.setLevel(logging.DEBUG)
        fh: logging.FileHandler = logging.FileHandler(
            filename=filename, mode="a", delay=False
        )
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        self.logger.addHandler(fh)

    def __del__(self):
        pass

    def read(self) -> list[str]:
        try:
            return_value: list[str] = []
            with open(self.filename) as f:
                for line in f.readlines():
                    return_value.append(line)
            return return_value
        except Exception as e:
            logging.error(e)
            raise e

    def write(self, text: str) -> None:
        try:
            self.logger.info(text)
        except Exception as e:
            logging.error(e)
            raise e
