import pathlib as pth
import typing as typ

# -- CREDENTIALS --

SCOPES: typ.List[str] = ['https://www.googleapis.com/auth/gmail.readonly']
PATH_CREDENTIALS_DATA: pth.Path = pth.Path(__file__).parent / "GmailApiInteraction" / "Credentials" / "data"

# -- OTHERS --

SEARCH_STRING_LIDER: str = "from:app lider subject:gracias por comprar en lider"
PAYABLE_PRODUCTS: typ.List[str] = ["cerveza",
                                   "gin",
                                   "vodka",
                                   "leche",
                                   "isotonica",
                                   "bebida"]
ROOT_LOCAL_SETTLEMENTS: pth.Path = pth.Path(__file__).parents[1] / "Outputs" / "settlements"
