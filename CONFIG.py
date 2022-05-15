import pathlib as pth

SEARCH_STRING_LIDER: str = "from:app lider subject:gracias por comprar en lider"
PAYABLE_PRODUCTS: [str] = ["cerveza",
                           "gin",
                           "vodka",
                           "leche",
                           "isotonica",
                           "bebida"]
ROOT_LOCAL_SETTLEMENTS: pth.Path = pth.Path(__file__).parent / "settlements"
