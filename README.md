# PythonWebHarvest

A Python-based web data scraping suite for harvesting Chinese novels (with full chapter support) and beyond. Features built-in anti-scraping measures — dynamic User-Agent rotation, rate limiting, retry logic — and a modular framework easily extendable to scrape anime sites, image galleries, APIs, and more.

---

## Table of Contents

- [Branches](#branches)

- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

---

## Branches

- **novel**: Basic scraper without anti-scraping. [novel branch](https://github.com/yourusername/PythonWebHarvest/tree/novel)

## Features

- **Modular Scripts**: Separate entry points for basic and protected sites.
- **Chapter-by-Chapter Download**: Automatically follows "Next Page" links to collect full text.
- **Anti-Scraping Measures** (_novelBiliBili_ only):
  - Dynamic User-Agent via `fake_useragent`.
  - Rate limiting with randomized delays.
  - Automatic retry with exponential backoff for transient failures.
- **Easy Configuration**: Set `START_URL` and `OUTPUT_FILE` at the top of each script.
- **Extensible Framework**: Add new scrapers for anime, image galleries, or APIs by following the same pattern.

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

