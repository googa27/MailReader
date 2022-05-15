import typing as typ
import pandas as pd
import datetime as dt

import src.CONFIG as CFG
import src.GmailApiInteraction.GmailController as gctl
import src.Parsers.GmailParsers as gprs
import src.LocalInteractions.SettlementManager as sman


class Accountant:

    def __init__(self):
        self._gmailController = gctl.GmailController()
        self._settlementsManager = sman.SettlementsManager()

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
                         dateStart: dt.date = dt.date.min) -> typ.Dict[dt.date, pd.DataFrame]:
        msgs = self._gmailController.get_raw_messages()
        datet_to_msgs = {gprs.GmailMessageParser.get_date_header(msg): msg
                         for msg in msgs}
        dt_to_df = {datet.date(): gprs.GmailProductParser.get_df_products(msg)
                    for datet, msg in sorted(datet_to_msgs.items(),
                                             key=lambda item: item[0])
                    if datet.date() > dateStart}
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
