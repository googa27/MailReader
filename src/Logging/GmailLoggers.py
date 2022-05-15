import typing as typ
import bs4


class GmailLogger:
    @staticmethod
    def printSeparator() -> None:
        print("\n" + "#" * 20 + "\n")

    @classmethod
    def describeObject(cls, obj: typ.Any) -> None:
        print(f"OBJECT: {obj}")
        print(f"OBJECT TYPE: {type(obj)}")
        print(f"METHODS AND ATTRIBUTES OF OBJECT:\n")
        for method in dir(obj):
            if method[0] != "_":
                print(method)

        cls.printSeparator()


class GmailMessageLogger(GmailLogger):
    @classmethod
    def printTagChildren(cls,
                         tag: bs4.element.Tag):
        cls.printSeparator()
        print(f"TAG NAME: {tag.name}")
        print(f"TAG TYPE: {type(tag)}")
        print(f"CHILDREN TYPES: {[type(e) for e in tag.children]}")
        print(f"CHILDREN NAMES: {[e.name for e in tag.children]}")
        cls.printSeparator()
