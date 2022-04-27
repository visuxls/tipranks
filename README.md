# TipRanks

Python module to interact with TipRanks API.

## Installation
From PyPi
```
pip install tipranks
```
For development
```
git clone https://github.com/visuxls/tipranks
```
## Features
- Support for the majority of TipRanks API endpoints (create an issue if I missed any)
- Automated browser login via Selenium

## To-Do
- [ ] `Login`: Implement request based login
- [ ] `Filtered results`: Implement filtered results

## Usage
![Usage](https://i.imgur.com/gs48kJN.png)

## Supported Methods
```.top_analyst_stocks()```

```.top_smart_score_stocks()```

```.top_insider_stocks()```

```.stock_screener()```

```.top_online_growth_stocks()```

```.trending_stocks()```

```.top_experts(expert_type="analyst")```

```.anaylst_projection(ticker="TSLA")```

```.stock_summary(ticker="TSLA")```

```.news_sentiment(ticker="TSLA")```