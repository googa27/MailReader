import os.path
import typing as typ
import base64
import bs4
import pandas as pd
import datetime as dt
import unidecode as unid
import pathlib as pth

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery as gdsc
from googleapiclient.errors import HttpError
import googleapiclient.http as ghttp

import CONFIG as CFG


################# LOGGERS #################


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

    # for msg in msgs[:2]:
    #     msg_dict = msg.execute()
    #     print(msg_dict["payload"].keys())
    #     print(len(msg_dict["payload"]["parts"]))
    #     print(msg_dict["payload"]["parts"][1].keys())
    #     body = msg_dict["payload"]["parts"][1]["body"]["data"]
    #     html_body = base64.urlsafe_b64decode(body)
    #     print(f"HTML BODY TYPE: {type(html_body)}")
    #     print(html_body)


################# PARSERS #################


class GmailMessageParser:
    _DATE_HEADER_FORMAT = "%a, %d %b %Y %X %z (%Z)"

    @staticmethod
    def decode_body(raw_message: ghttp.HttpRequest) -> str:
        msg_dict = raw_message.execute()
        print(msg_dict["payload"]["parts"][1].keys())
        # print(msg_dict["payload"]["parts"][1]["headers"])
        # print(msg_dict["payload"]["parts"][0])
        print("#" * 20)
        body = msg_dict["payload"]["parts"][1]["body"]["data"]
        return base64.urlsafe_b64decode(body).decode("utf-8")

    @staticmethod
    def get_df_products(raw_message: ghttp.HttpRequest) -> pd.DataFrame:
        return GmailProductParser.get_df_products(raw_message=raw_message)

    @classmethod
    def get_date_header(cls,
                        raw_message: ghttp.HttpRequest) -> dt.datetime:
        """

        Args:
            raw_message:

        Returns: Date in the 'header' field in the google message.

        """
        msg_dict = raw_message.execute()
        raw_date = [d for d in msg_dict["payload"]["headers"] if d["name"] == "Date"][0]["value"]
        print(raw_date)
        return dt.datetime.strptime(raw_date,
                                    cls._DATE_HEADER_FORMAT)

    @classmethod
    def get_info_tables(cls,
                        raw_message: ghttp.HttpRequest) -> [bs4.element.Tag]:
        msg_b: str = cls.decode_body(raw_message=raw_message)
        soup = bs4.BeautifulSoup(msg_b,
                                 "html5lib")
        html = soup.find("html")
        body = html.find("body")
        center = body.find("center")
        tables = center.select("div > table")
        print(f"LENGHT OF TABLES: {len(tables)}")
        for i, tab in enumerate(tables):
            GmailMessageLogger.printSeparator()
            print(f"TABLE INDEX: {i}")
            print(tab)
        return tables

    # @staticmethod
    # def get_date(raw_message: ghttp.HttpRequest):
    #     msg_dict = raw_message.execute()
    #     text_body = msg_dict["payload"]["parts"][1]["body"]["data"]
    #     text_body = base64.urlsafe_b64decode(text_body)
    #     return bs4.BeautifulSoup(text_body, "html.parser")


class GmailProductParser:

    @classmethod
    def get_df_products(cls, raw_message: ghttp.HttpRequest) -> pd.DataFrame:
        df_products = pd.DataFrame([cls._parse_table_element(table)
                                    for table in cls._get_product_tables(raw_message=raw_message)])
        df_products["unitary_price"] = df_products["total_price"] / df_products["units"]
        return df_products

    @staticmethod
    def _get_product_tables(raw_message: ghttp.HttpRequest) -> [bs4.element.Tag]:
        msg_dict = raw_message.execute()
        text_body = msg_dict["payload"]["parts"][0]["body"]["data"]
        text_body = base64.urlsafe_b64decode(text_body)
        return bs4.BeautifulSoup(text_body, "html.parser").select("div > table")

    @staticmethod
    def _parse_td_1(td: bs4.element.Tag) -> {str: int}:
        return {"units": int(td.get_text())}

    @staticmethod
    def _parse_td_2(td: bs4.element.Tag) -> {str: typ.Union[str, float]}:
        divs = td.find_all("div")
        brand_product = {k.strip(): unid.unidecode(v.strip())
                         for k, v in zip(["brand", "product"],
                                         divs[0].get_text().split("·"))
                         }
        weight_unit_split = divs[1].get_text().split(" ")
        if len(weight_unit_split) == 2:
            weight_unit = {k.strip(): v.strip()
                           for k, v in zip(["unitary_content", "content_units"],
                                           weight_unit_split)
                           }
        else:
            weight_unit = {k.strip(): v
                           for k, v in zip(["unitary_content", "content_units"],
                                           [1, divs[1].get_text()])
                           }
        return brand_product | weight_unit

    @staticmethod
    def _parse_td_3(td: bs4.element.Tag) -> {str: int}:
        clean_price_string = td.get_text().replace(".", "").replace("$", "")
        return {"total_price": int(clean_price_string)}

    @classmethod
    def _parse_table_element(cls,
                             table: bs4.element.Tag) -> {str: typ.Union[str, int]}:
        tds = table.find_all("td")
        return cls._parse_td_1(tds[1]) | cls._parse_td_2(tds[2]) | cls._parse_td_3(tds[3])


################# API INTERACTIONS #################


class GmailCredentialManager:
    _SCOPES: [str] = ['https://www.googleapis.com/auth/gmail.readonly']
    _PATH_CREDENTIALS: str = "credentials.json"
    _PATH_TOKEN: str = "token.json"

    @classmethod
    def _login(cls, creds) -> Credentials:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cls._PATH_CREDENTIALS,
                                                             cls._SCOPES)
            creds = flow.run_local_server(port=0)
        return creds

    @classmethod
    def _save_creds(cls, creds) -> None:
        with open(cls._PATH_TOKEN, "w") as token:
            token.write(creds.to_json())

    @classmethod
    def getCredentials(cls) -> Credentials:
        creds = None
        if os.path.exists(cls._PATH_TOKEN):
            creds = Credentials.from_authorized_user_file(cls._PATH_TOKEN,
                                                          cls._SCOPES)
        if not creds or not creds.valid:
            creds = cls._login(creds)
            cls._save_creds(creds)
        print(f"TYPE OF CREDS: {type(creds)}")
        return creds


class GmailController:

    def __init__(self):
        try:
            creds = GmailCredentialManager.getCredentials()
            service: gdsc.Resource = gdsc.build("gmail",
                                                "v1",
                                                credentials=creds)
            self._users_resource: gdsc.Resource = service.users()
            print(self._users_resource)
        except HttpError as error:
            print(f"An error occured: {error}")

    def _get_message_ids(self,
                         q: str) -> [{str, str}]:
        """

        Args:
            q: gmail query.

        Returns: messages ids corresponding to query

        """
        try:
            http_response = self._users_resource.messages().list(userId="me",
                                                                 q=q).execute()
            return http_response["messages"]

        except HttpError as error:
            print(f"An error occured: {error}")

    def get_raw_messages(self,
                         q: str = CFG.SEARCH_STRING_LIDER) -> [ghttp.HttpRequest]:
        try:
            return [self._users_resource.messages().get(userId="me",
                                                        id=ident["id"])
                    for ident in self._get_message_ids(q=q)]
        except HttpError as error:
            print(f"An error occured: {error}")

    def get_labels(self) -> None:
        """
        Shows basic usage of the Gmail API . Lists user's Gmail labels.

        Returns:

        """

        try:

            results = self._users_resource.labels().list(userId="me").execute()
            labels = results.get("labels", [])

            if not labels:
                print("No labels found.")
                return
            print("Labels:")
            for label in labels:
                print(label["name"])
        except HttpError as error:
            print(f"Type of error thingy {type(error)}")
            print(f"An error occured: {error}")


################# LOCAL DATA INTERACTIONS #################
class SettlementsManager:
    _DATE_FILENAME_FORMAT = "%Y-%m-%d"

    def __init__(self,
                 root_settlements: pth.Path = CFG.ROOT_LOCAL_SETTLEMENTS):
        self._root_settlements: pth.Path = root_settlements

    def get_latest_settlement_date(self) -> dt.date:
        files = self._root_settlements.glob("*.xlsx")
        dates = [dt.datetime.strptime(file.stem, self._DATE_FILENAME_FORMAT).date()
                 for file in files]
        return max(dates)

    def get_save_path(self, date: dt.date = dt.date.today()) -> pth.Path:
        return self._root_settlements / f"{date.strftime(self._DATE_FILENAME_FORMAT)}.xlsx"


################# ACCOUNTANT #################

class Accountant:

    def __init__(self):
        self._gmailController = GmailController()
        self._settlementsManager = SettlementsManager()

    def get_latest_settlement(self,
                              save: bool = False,
                              filter_payables=True) -> typ.Optional[pd.DataFrame]:
        dt_to_df = self._get_product_dfs(dateStart=self._settlementsManager.get_latest_settlement_date())
        if not dt_to_df:
            print("No data for Settlement.")
            return None

        settlement = pd.concat(list(dt_to_df.values()))
        if filter_payables:
            settlement = self._filter_payable_products(settlement)

        settlement = self._add_total_row(settlement)

        if save:
            settlement.to_excel(self._settlementsManager.get_save_path(),
                                index=False)
        return settlement

    def _get_product_dfs(self,
                         dateStart: dt.date = dt.date.min) -> {dt.date: pd.DataFrame}:
        msgs = self._gmailController.get_raw_messages()
        datet_to_msgs = {GmailMessageParser.get_date_header(msg): msg
                         for msg in msgs}
        dt_to_df = {datet.date(): GmailProductParser.get_df_products(msg)
                    for datet, msg in sorted(datet_to_msgs.items(),
                                             key=lambda item: item[0])
                    if datet.date() >= dateStart}
        for date, df in dt_to_df.items():
            df["date"] = date
        return dt_to_df

    @staticmethod
    def _filter_payable_products(df: pd.DataFrame) -> pd.DataFrame:
        mask_payable = df["product"].str.lower().apply(lambda s: any(product in s
                                                                     for product in CFG.PAYABLE_PRODUCTS)
                                                       )
        return df[mask_payable]

    @staticmethod
    def _add_total_row(df: pd.DataFrame) -> pd.DataFrame:
        row_total = {col: "TOTAL" for col in df.columns
                     if col != "total_price"}
        row_total = row_total | {"total_price": df["total_price"].sum()}
        row_total = pd.DataFrame(row_total,
                                 index=["TOTAL"])
        return pd.concat([df,
                          row_total])


if __name__ == '__main__':
    # gc = GmailController()
    # msgs = gc.get_raw_messages(q=CFG.SEARCH_STRING_LIDER)
    #
    # date = GmailMessageParser.get_date_header(msgs[0])
    # print(date)
    # df = GmailProductParser.get_df_products(msgs[0])
    # print(df)
    # print(df.iloc[0])
    #
    # lsm = SettlementsManager()
    # print(lsm.get_latest_settlement_date())

    accountant = Accountant()
    # print(accountant.get_product_dfs())
    settlement = accountant.get_latest_settlement(save=True)
    print(settlement)

    # msg_dict = msgs[0].execute()
    # date = [d for d in msg_dict["payload"]["headers"] if d["name"] == "Date"][0]["value"]
    # print(date)

    # for msg in msgs[:1]:
    #     soup = GmailMessageParser.get_date(msg)
    #     print(type(soup))
    #     print(soup.prettify())
    # print(soup.find_all("div", id=":2k"))

    # for msg in msgs[:1]:
    #     # tables = GmailMessageParser.get_product_tables(msg)
    #     df = GmailMessageParser.get_df_products(raw_message=msg)
    #     GmailLogger.printSeparator()
    #     print(df)
    #     GmailLogger.printSeparator()
    #     print(df.describe())
    #     GmailLogger.printSeparator()
    #     print(df.info())
    #     GmailLogger.printSeparator()
    #     print(df.iloc[0])

    # for tab in tables[:1]:
    #     print(GmailMessageParser.parse_table_element(table=tab))
    # tds = tab.find_all("td")
    # for i, td in enumerate(tds):
    #     print(f"{i}-th TD")
    #     print(td.prettify())
    # print(tab.get_text())
    # msg_b: str = GmailMessageParser.decode_body(msg)
    # # print(msg_b)
    # soup = bs4.BeautifulSoup(msg_b, "html.parser")
    # print(len(list(soup.children)))
    # # divs = soup.find_all("div")
    # print([t.name for t in soup.children])
    # divs = soup.find_all("div", recursive=False)
    # tables = soup.select("div > table")  # soup.find_all("table")
    # print(f"N DIVS: {len(divs)}")
    # print(f"N TABLES: {len(tables)}")
    # for div in divs:
    #     print(div.get_text())
    # print(len(divs))

    GmailLogger.printSeparator()

    if False:
        for msg in msgs[:1]:
            msg_b: str = GmailMessageParser.decode_body(msg)
            # msg_b = msg_b.replace("\n", "").replace("\t", "")
            # print(str(msg_b))

            GmailLogger.printSeparator()

            soup = bs4.BeautifulSoup(msg_b,
                                     "html5lib")
            GmailMessageLogger.printTagChildren(soup)

            GmailLogger.printSeparator()

            html = soup.find("html")
            GmailMessageLogger.printTagChildren(html)

            GmailLogger.printSeparator()

            head = html.find("head")
            body = html.find("body")
            GmailMessageLogger.printTagChildren(head)
            GmailMessageLogger.printTagChildren(body)

            GmailLogger.printSeparator()

            center = body.find("center")
            GmailMessageLogger.printTagChildren(center)

            GmailMessageLogger.printSeparator()

            tables = center.select("div > table")
            print(f"LENGHT OF TABLES: {len(tables)}")
            for i, tab in enumerate(tables):
                GmailMessageLogger.printSeparator()
                print(f"TABLE INDEX: {i}")
                print(tab)
                # GmailMessageLogger.printSeparator()

            # table = center.find("table")
            # GmailMessageLogger.printTagChildren(table)
            # print(table)

            # print(list(center.children)[-1])

            # print(soup.find_all("div", id=":2k"))
            # print(list(soup.children)[-1])
            # print(len(soup.find_all("div", id=":2k")))
            # print(len(soup.find_all("center", style="background:#fafafa")))
            # print(len(soup.find_all("table",
            #                         align="center",
            #                         border="0",
            #                         cellpadding="0",
            #                         cellspacing="0",
            #                         width="100%")))
            # divs = soup.find_all("div", recursive=False)
            # print(len(divs))
            # print([type(x) for x in soup.children])
            # print(list(soup.children)[1])
            # print([tag.name for tag in soup.children])
            # print(soup.find_all("div"))

    # gc.get_labels()

# \:2k > div:nth-child(2) > center
