import smtplib
import requests
import lxml
from bs4 import BeautifulSoup

MY_EMAIL = "pasan7989@yahoo.com"
MY_PASSWORD = "vkyojatvkjghoqkm"
TARGET_PRICE = 150


class AmazonPriceTracker:
    def __init__(self):
        self.amazon_url = "https://www.amazon.com/Calphalon-Classic-10-Piece-Nonstick-Cookware/dp/B01APP1W2O/ref=sr_1_1?crid=2ULBSDJRUNYC5&keywords=pots+and+pans+set&nav_sdd=aps&qid=1659423268&refinements=p_n_feature_four_browse-bin%3A2242056011&rnid=2242047011&s=kitchen&sprefix=pots&sr=1-1"
        self.amazon_headers = {
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        self.check_and_send()

    def check_and_send(self):
        """Check whether the current price of the product is below my target price, if so send an email."""
        current_price = self.get_price()
        if current_price < TARGET_PRICE:
            self.send_mail(current_price)

    def get_price(self) -> float:
        """Return the current price of the product"""
        response = requests.get(url=self.amazon_url, headers=self.amazon_headers)
        website_html = response.text
        soup = BeautifulSoup(website_html, "lxml")
        price = float(soup.select_one(selector="span .a-offscreen").getText()[1:])
        return price

    def send_mail(self, price):
        """Send an email informing about the price drop."""
        with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                                msg=f"Subject:Price Drop!\n\nThe product is now ${price}, below your target price. "
                                    f"Buy Now!!!")


if __name__ == "__main__":
    amazon_price_tracker = AmazonPriceTracker()
