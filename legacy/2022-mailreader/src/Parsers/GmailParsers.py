import typing as typ
import base64
import bs4
import pandas as pd
import datetime as dt
import unidecode as unid

import googleapiclient.http as ghttp

import src.Logging.GmailLoggers as glog


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
                        raw_message: ghttp.HttpRequest) -> typ.List[bs4.element.Tag]:
        msg_b: str = cls.decode_body(raw_message=raw_message)
        soup = bs4.BeautifulSoup(msg_b,
                                 "html5lib")
        html = soup.find("html")
        body = html.find("body")
        center = body.find("center")
        tables = center.select("div > table")
        print(f"LENGHT OF TABLES: {len(tables)}")
        for i, tab in enumerate(tables):
            glog.GmailMessageLogger.printSeparator()
            print(f"TABLE INDEX: {i}")
            print(tab)
        return tables


class GmailProductParser:

    @classmethod
    def get_df_products(cls, raw_message: ghttp.HttpRequest) -> pd.DataFrame:
        df_products = pd.DataFrame([cls._parse_table_element(table)
                                    for table in cls._get_product_tables(raw_message=raw_message)])
        df_products["unitary_price"] = df_products["total_price"] / df_products["units"]
        return df_products

    @staticmethod
    def _get_product_tables(raw_message: ghttp.HttpRequest) -> typ.List[bs4.element.Tag]:
        msg_dict = raw_message.execute()
        text_body = msg_dict["payload"]["parts"][0]["body"]["data"]
        text_body = base64.urlsafe_b64decode(text_body)
        return bs4.BeautifulSoup(text_body, "html.parser").select("div > table")

    @staticmethod
    def _parse_td_1(td: bs4.element.Tag) -> typ.Dict[str, int]:
        return {"units": int(td.get_text())}

    @staticmethod
    def _parse_td_2(td: bs4.element.Tag) -> typ.Dict[str, typ.Union[str, float]]:
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
    def _parse_td_3(td: bs4.element.Tag) -> typ.Dict[str, int]:
        clean_price_string = td.get_text().replace(".", "").replace("$", "")
        return {"total_price": int(clean_price_string)}

    @classmethod
    def _parse_table_element(cls,
                             table: bs4.element.Tag) -> typ.Dict[str, typ.Union[str, int]]:
        tds = table.find_all("td")
        return cls._parse_td_1(tds[1]) | cls._parse_td_2(tds[2]) | cls._parse_td_3(tds[3])
