# Simple Scraper API

A minimal HTTP service that accepts a single `POST /scrape/start` request with a JSON `link` body parameter, runs a remote Selenium-based scrape inside your configured Docker environment, and returns the scraped page HTML.

---

## Features

* Single endpoint: `POST /scrape/start` (JSON body `{ "link": "<url>" }`)
* Simple API key gating
* Runs Chrome inside a remote Selenium container (no setup required)
* Returns:

  ```json
  {
    "success": true|false,
    "data": "<body HTML string or null>",
    "error": "<error message or null>"
  }
  ```
  
---

## Requirements

* Docker installed on the host
* (Optional but recommended) Docker Compose
* Network connectivity between the scraper container and the Selenium container (Docker network)

---

## Environment

Create a `.env` file using these variables:

```
DEBUG=True
API_KEY=
DOCKER_NETWORK_NAME=
SELENIUM_PASSWORD=
```

**Notes**

* `API_KEY` — secret key that the API expects in requests.
* `DOCKER_NETWORK_NAME` — name of the Docker network used to connect scraper and Selenium containers.
* `SELENIUM_PASSWORD` — optional password if your Selenium setup requires one.

---

## API

### `POST /scrape/start`

Start a scrape job for a given `link`.

* **URL**: `/scrape/start`
* **Method**: `POST`
* **Headers**:

  * `Content-Type: application/json`
  * `X-API-KEY: <API_KEY>` (if set)
* **Body**:

  ```json
  {
    "link": "https://example.com"
  }
  ```

### Success response (200)

```json
{
  "success": true,
  "data": "<body innerHTML string>",
  "error": null
}
```

### Failure response (4xx / 5xx)

```json
{
  "success": false,
  "data": null,
  "error": "detailed error message"
}
```

---

## Example `curl` usage

```bash
curl -X POST "http://localhost:8000/scrape/start" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_api_key_here" \
  -d '{"link": "https://example.com"}'
```

Sample response:

```json
{
  "success": true,
  "data": "<div>...page body html...</div>",
  "error": null
}
```
