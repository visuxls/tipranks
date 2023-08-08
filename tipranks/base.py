from .errors import (
	TipRanksStatusCodeError,
	TipRanksArgumentError,
	TipRanksRequestError
)
from typing import Optional, Any
import requests
import time


EXPERT_TYPES = [
	"analyst",
	"blogger",
	"insider",
	"institutional",
	"user"
]


class TipRanks:
	def __init__(self, email: str, password: str) -> None:
		self._base_url: str = "https://mobile.tipranks.com"
		self._session: requests.sessions.Session = requests.Session()

		self.login(email=email, password=password)

	def __request(
		self, method: str, endpoint: str, params: Optional[dict] = None, json: Optional[dict] = None, login: Optional[bool] = None
	) -> Any:
		try:
			response = self._session.request(
				method=method.upper(),
				url=f"{self._base_url}{endpoint}",
				headers={
					"accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
					"content-type": "application/json; charset=UTF-8",
					"accept-encoding": "gzip",
					"x-platform": "iphone",
					"user-agent": "TipRanksApp/17 CFNetwork/1390 Darwin/22.0.0",
					"accept-language": "en-US,en;q=0.9"
				},
				json=json,
				params=params
			)
		except:
			raise TipRanksRequestError("Request Timed Out")

		if login:
			return response.status_code

		return response.json()

	def login(self, email: str, password: str) -> None:
		status_code = self.__request(
			method="POST",
			endpoint="/api/iOS/login2",
			json={
				"email": email,
				"password": password
			},
			login=True
		)

		if status_code != 200:
			raise TipRanksStatusCodeError(f"Failed To Login, Status Code: {status_code}")

	def get_top_analyst_stocks(self) -> list:
		return self.__request(
			method="GET",
			endpoint="/api/stocks/getMostRecommendedStocks/",
			params={
				"benchmark": "1",
				"period": "3",
				"country": "US",
				"break": int(time.time())
			}
		)

	def get_top_smart_score_stocks(self) -> list:
		return self.__request(
			method="GET",
			endpoint="/api/Screener/GetStocks/",
			params = {
				"break": int(time.time()),
				"country": "US",
				"page": "1",
				"sortBy": "1",
				"sortDir": "2",
				"tipranksScore": "5"
			}
		)

	def get_top_insider_stocks(self) -> list:
		return self.__request(
			method="GET",
			endpoint="/api/insiders/getTrendingStocks/",
			params={
				"benchmark": "1",
				"period": "3",
				"country": "US",
				"break": int(time.time())
			}
		)

	def get_stock_screener(self) -> list:
		return self.__request(
			method="GET",
			endpoint="/api/Screener/GetStocks/",
			params = {
				"break": int(time.time()),
				"country": "US",
				"page": "1",
				"sortBy": "1",
				"sortDir": "2",
			}
		)

	def get_top_online_growth_stocks(self) -> list:
		return self.__request(
			method="GET",
			endpoint="/api/websiteTraffic/screener",
			params={
				"country": "us"
			}
		)

	def get_trending_stocks(self) -> list:
		return self.__request(
			method="GET",
			endpoint="/api/stocks/gettrendingstocks/",
			params={
				"daysago": "30",
				"which": "most",
				"country": "us",
				"break": int(time.time())
			}
		)

	def get_top_experts(self, expert_type: str) -> list:
		if expert_type.lower() == "analyst":
			params = {
				"expertType": "analyst",
				"numExperts": "100",
				"period": "year",
				"benchmark": "none"
			}
		else:
			params = {
				"expertType": expert_type,
				"numExperts": "100"
			}

		return self.__request(
			method="GET",
			endpoint="/api/experts/GetTop25Experts/",
			params=params
		)

	def get_analyst_projection(self, ticker: str) -> list:
		return self.__request(
			method="GET",
			endpoint="/api/compare/analystRatings/tickers/",
			params={
				"tickers": ticker.lower()
			}
		)

	def get_news_sentiment(self, ticker: str) -> list:
		return self.__request(
			method="GET",
			endpoint="/api/stocks/getNews/",
			params={
				"ticker": ticker
			}
		)

	def top_analyst_stocks(self) -> dict:
		"""
		Returns the current recommended stocks. The list is
		curated based on stocks with a 'Strong Buy' or
		'Strong Sell' rating consensus.
		"""
		body = self.get_top_analyst_stocks()

		return body

	def top_smart_score_stocks(self) -> list:
		"""
		Returns the best stocks according to the TipRanks Smart Score.
		This unique score measures stocks on their potential to
		outperform the market, based on 8 key factors.
		"""
		body = self.get_top_smart_score_stocks()

		return body

	def top_insider_stocks(self) -> list:
		"""
		Returns the current insider stocks. The list is
		curated based on insider trading.
		"""
		body = self.get_top_insider_stocks()

		return body

	def stock_screener(self) -> list:
		"""
		Returns unique signals and data. See a comprehensive
		overview of stock performance.
		"""
		body = self.get_stock_screener()

		return body

	def top_online_growth_stocks(self) -> list:
		"""
		Discover publicly traded companies with trending websites.
		These top websites have the highest website traffic
		increases over the past month.
		"""
		body = self.get_top_online_growth_stocks()

		return body

	def trending_stocks(self) -> list:
		"""
		Returns the current trending stocks. The list is
		curated based on if a stock has been rated by 3 or
		more analysts in the last few days.
		"""
		body = self.get_trending_stocks()

		return body

	def top_experts(self, expert_type: str) -> list:
		"""
		Returns the current top experts. TipRanks shows 
		Analysts, Bloggers, Corporate Insiders, Hedge Fund
		Managers, Research Firms, and Individual Investors.
		"""
		if expert_type not in EXPERT_TYPES:
			raise TipRanksArgumentError(f"{expert_type} is not a valid choice. The valid choices are {', '.join(EXPERT_TYPES)}.")

		body = self.get_top_experts(expert_type)

		return body

	def anaylst_projection(self, ticker: str) -> list:
		"""
		Returns all of the available analyst projections
		for a given ticker.
		"""
		body = self.get_analyst_projection(ticker)

		return body

	def news_sentiment(self, ticker: str) -> list:
		"""
		Returns the latest news articles and its sentiment for 
		a given ticker.
		"""
		data = self.get_news_sentiment(ticker)

		return data