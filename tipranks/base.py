from tipranks.errors import (
	TipRanksArgsError,
	TipRanksRequestError
)
from .login import TipRanksLogin
import requests
import time


_BASE_URL_ = "https://www.tipranks.com/api"
_AZURE_URL_ = "https://tr-frontend-cdn.azureedge.net"

EXPERT_TYPES = [
	"analyst",
	"blogger",
	"insider",
	"institutional",
	"user"
]


class TipRanks:
	def __init__(self, email: str, password: str) -> None:
		tipranks = TipRanksLogin(
			email=email,
			password=password
		)
		self.cookies = tipranks.login()

	def request(self, method: str, url: str, params: dict) -> list:
		try:
			response = requests.request(
				method.upper(),
				url,
				headers = {
					"authority": "www.tipranks.com",
					"accept": "*/*",
					"accept-language": "en-US,en;q=0.9",
					"referer": "https://www.tipranks.com/",
					"sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"101\", \"Google Chrome\";v=\"101\"",
					"sec-ch-ua-mobile": "?0",
					"sec-ch-ua-platform": "\"Windows\"",
					"sec-fetch-dest": "empty",
					"sec-fetch-mode": "cors",
					"sec-fetch-site": "same-origin",
					"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
					"cookie": self.cookies
				},
				params = params
			)

		except:
			raise TipRanksRequestError("Request Timed Out")

		return response.json()

	def get_top_analyst_stocks(self) -> list:
		return self.request(
			method = "GET",
			url = f"{_BASE_URL_}/stocks/getMostRecommendedStocks/",
			params = {
				"benchmark": "1",
				"period": "3",
				"country": "US",
				"break": ""
			}
		)

	def get_top_smart_score_stocks(self) -> list:
		return self.request(
			method = "GET",
			url = f"{_BASE_URL_}/Screener/GetStocks/",
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
		return self.request(
			method = "GET",
			url = f"{_BASE_URL_}/insiders/getTrendingStocks/",
			params = {
				"benchmark": "1",
				"period": "3",
				"country": "US",
				"break": ""
			}
		)

	def get_stock_screener(self) -> list:
		return self.request(
			method = "GET",
			url = f"{_BASE_URL_}/Screener/GetStocks/",
			params = {
				"break": int(time.time()),
				"country": "US",
				"page": "1",
				"sortBy": "1",
				"sortDir": "2",
			}
		)

	def get_top_online_growth_stocks(self) -> list:
		return self.request(
			method = "GET",
			url = f"{_BASE_URL_}/websiteTraffic/screener",
			params = {
				"country": "us"
			}
		)

	def get_trending_stocks(self) -> list:
		return self.request(
			method = "GET",
			url = f"{_BASE_URL_}/stocks/gettrendingstocks/",
			params = {
				"daysago": "30",
				"which": "most",
				"country": "us",
				"break": ""
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

		return self.request(
			method = "GET",
			url = f"{_BASE_URL_}/experts/GetTop25Experts/",
			params = params
		)

	def get_analyst_projection(self, ticker: str) -> list:
		return self.request(
			method = "GET",
			url = f"{_BASE_URL_}/compare/analystRatings/tickers/",
			params = {
				"tickers": ticker.lower()
			}
		)

	def get_stock_summary(self, ticker: str) -> list:
		return self.request(
			method = "GET",
			url = f"{_AZURE_URL_}/bff/prod/stock/{ticker.lower()}/payload.json",
			params = {}
		)

	def get_news_sentiment(self, ticker: str) -> list:
		return self.request(
			method = "GET",
			url = f"{_BASE_URL_}/stocks/getNews/",
			params = {
				"ticker": ticker
			}
		)

	def top_analyst_stocks(self) -> list:
		"""
		Returns the current recommended stocks. The list is
		curated based on stocks with a 'Strong Buy' or 
		'Strong Sell' rating consensus.
		"""
		data = self.get_top_analyst_stocks()

		return data

	def top_smart_score_stocks(self) -> list:
		"""
		Returns the best stocks according to the TipRanks Smart Score.
		This unique score measures stocks on their potential to
		outperform the market, based on 8 key factors.
		"""
		data = self.get_top_smart_score_stocks()

		return data

	def top_insider_stocks(self) -> list:
		"""
		Returns the current insider stocks. The list is
		curated based on insider trading.
		"""
		data = self.get_top_insider_stocks()

		return data

	def stock_screener(self) -> list:
		"""
		Returns unique signals and data. See a comprehensive
		overview of stock performance.
		"""
		data = self.get_stock_screener()

		return data

	def top_online_growth_stocks(self) -> list:
		"""
		Discover publicly traded companies with trending websites.
		These top websites have the highest website traffic
		increases over the past month.
		"""
		data = self.get_top_online_growth_stocks()

		return data

	def trending_stocks(self) -> list:
		"""
		Returns the current trending stocks. The list is
		curated based on if a stock has been rated by 3 or
		more analysts in the last few days.
		"""
		data = self.get_trending_stocks()

		return data

	def top_experts(self, expert_type: str) -> list:
		"""
		Returns the current top experts. TipRanks shows 
		Analysts, Bloggers, Corporate Insiders, Hedge Fund
		Managers, Research Firms, and Individual Investors.
		"""
		if expert_type not in EXPERT_TYPES:
			raise TipRanksArgsError(f"{expert_type} is not a valid choice. The valid choices are {', '.join(EXPERT_TYPES)}.")

		data = self.get_top_experts(expert_type)

		return data

	def anaylst_projection(self, ticker: str) -> list:
		"""
		Returns all of the available analyst projections
		for a given ticker.
		"""
		data = self.get_analyst_projection(ticker)

		return data

	def stock_summary(self, ticker: str) -> list:
		"""
		Returns a summary of the current stock's standing
		with analysts. Provides consensus and best_consensus
		ratings.
		"""
		data = self.get_stock_summary(ticker)

		return data

	def news_sentiment(self, ticker: str) -> list:
		"""
		Returns the latest news articles and its sentiment for 
		a given ticker.
		"""
		data = self.get_news_sentiment(ticker)

		return data