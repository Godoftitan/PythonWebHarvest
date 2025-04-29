# PythonWebHarvest

A Python-based web data scraping suite for harvesting Chinese novels (with full chapter support) and beyond. Features built-in anti-scraping measures — dynamic User-Agent rotation, rate limiting, retry logic — and a modular framework easily extendable to scrape anime sites, image galleries, APIs, and more.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [novel (Basic Scraper)](#novel-basic-scraper)
  - [novelBiliBili (Anti-Scraping)](#novelbilibili-anti-scraping)
- [Configuration](#configuration)
- [Extending to Other Sites](#extending-to-other-sites)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Modular Scripts**: Separate entry points for basic and protected sites.
- **Chapter-by-Chapter Download**: Automatically follows "Next Page" links to collect full text.
- **Anti-Scraping Measures** (_novelBiliBili_ only):
  - Dynamic User-Agent via `fake_useragent`.
  - Rate limiting with randomized delays.
  - Automatic retry with exponential backoff for transient failures.
- **Easy Configuration**: Set `START_URL` and `OUTPUT_FILE` at the top of each script.
- **Extensible Framework**: Add new scrapers for anime, image galleries, or APIs by following the same pattern.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PythonWebHarvest.git
   cd PythonWebHarvest
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate   # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### novel (Basic Scraper)

A simple scraper for Chinese novel sites without anti-bot protections.

```bash
python novel.py
```

- **START_URL**: The first chapter URL to begin scraping.
- **OUTPUT_FILE**: The target `.txt` file to save content.

### novelBiliBili (Anti-Scraping)

Enhanced scraper using `cloudscraper` and `fake_useragent` to bypass common protections.

```bash
python novelBiliBili.py
```

- Utilizes `cloudscraper.create_scraper` to handle Cloudflare.
- Retries on non-200 responses with exponential backoff.
- Randomized `time.sleep` between page requests (5–15 seconds).

## Configuration

Both scripts expose the following at the top:

```python
START_URL = "https://example.com/novel/1234/5678.html"
OUTPUT_FILE = "novel.txt"
MAX_RETRIES = 5  # only in novelBiliBili.py
```

Adjust these values as needed for different target sites.

## Extending to Other Sites

1. Copy one of the existing scripts into a new file (e.g., `animeCrawler.py`).
2. Update the parsing logic (`BeautifulSoup` selectors) to match the new site's HTML structure.
3. Configure anti-scraping (use `cloudscraper` + `fake_useragent`) or keep it basic.
4. Add any site-specific headers, cookies, or proxy logic in `safe_get`.

## Future Improvements

- **Proxy Support**: Rotate through proxy pools to avoid IP bans.
- **Asynchronous Requests**: Speed up scraping with `aiohttp` and `asyncio`.
- **CLI Interface**: Provide a command-line tool with flags for speed, output format, and site selection.
- **Data Export**: Support exporting to JSON, EPUB, or Markdown.

## Contributing

1. Fork the repo and create your branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
2. Commit your changes:
   ```bash
   git commit -m "Add feature X"
   ```
3. Push to the branch:
   ```bash
   git push origin feature/YourFeature
   ```
4. Submit a Pull Request.

Please ensure your code follows PEP8 and include tests where applicable.

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

