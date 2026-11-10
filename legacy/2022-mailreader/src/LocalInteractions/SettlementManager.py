import pathlib as pth
import datetime as dt

import src.CONFIG as CFG


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
