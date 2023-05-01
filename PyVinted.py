import requests, time, threading

class Vinted:

    def __init__(self, currency: int) -> None:
        '''Currencies (0: EUR, 1 USD) '''
        self.sizes = {"XS": 206, "S": 207, "M": 208, "L": 209, "XL": 210}
        self.currencies = ["EUR", "USD"]
        self.base_url = "https://www.vinted.com/api/v2"
        self.session = requests.session()
        self.currency = self.currencies[currency]

    def getHeaders(self):
        return {
            "content-type": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "fr,fr-FR;q=0.9,en;q=0.8,fr-FR;q=0.7",
            "cache-control": "no-cache",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
            }

    def InitVintedSession(self):
        self.session.get('https://www.google.fr/') # Prepare session Fingerprint
        self.session.get('https://vinted.com/', headers=self.getHeaders()) # Get main vinted cookies

    def search(self, search_text, order_type="", size="", max_price=999, page=1, max_items_per_page=24):
        head = self.getHeaders()
        search_text = search_text.replace(" ", "+")
        #head['cookie'] = f"v_udt={self.session.cookies.get_dict()['v_udt']}; v_sid={self.session.cookies.get_dict()['v_sid']}; _vinted_fr_session={self.session.cookies.get_dict()['_vinted_fr_session']}; anon_id={self.session.cookies.get_dict()['anon_id']}"
        url = self.base_url + "/catalog/items" + f"?search_text={search_text}&catalog_ids={f'&price_to={max_price}' if max_price > 0 else ''}&currency={self.currency}&color_ids=&brand_ids=&size_ids={size}&material_ids=&video_game_rating_ids=&status_ids=&order={order_type}&page={page}&per_page={max_items_per_page}"
        req = self.session.get(url, headers=head)
        print(str(req.json()))
        return req.json()