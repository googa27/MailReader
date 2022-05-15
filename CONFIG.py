import pathlib as pth
import typing as typ

SEARCH_STRING_LIDER: str = "from:app lider subject:gracias por comprar en lider"
PAYABLE_PRODUCTS: typ.List[str] = ["cerveza",
                                    "gin",
                                    "vodka",
                                    "leche",
                                    "isotonica",
                                    "bebida"]
ROOT_LOCAL_SETTLEMENTS: pth.Path = pth.Path(__file__).parent / "settlements"
