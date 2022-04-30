class MailReader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, *args, **kwargs):
        """
        Parses HTML within mail.

        Args:
            *args:
            **kwargs:

        Returns:

        """
        pass

class MailReaderLider(MailReader):
    pass

class MailReaderAgua(MailReader):
    pass