#############

import sys

for path in sys.path:
    print(path)

#############


import src.Logging.GmailLoggers as glog
import src.MainBackend.Accountant as acc

if __name__ == '__main__':

    accountant = acc.Accountant()
    settlement = accountant.get_latest_settlement(save=True)
    print(settlement)

    glog.GmailLogger.printSeparator()

    if False:
        for msg in msgs[:1]:
            msg_b: str = GmailMessageParser.decode_body(msg)

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
