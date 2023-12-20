# Web browser Proxy with Multi-threading

## Inspired by Computer Networking: A Top-Down Approach

---

## How to use

- This Proxy Server works only with HTTP protocols. If you
  try to use this proxy with HTTPS sites, you will typically
  see a 301 response in the cache.
- Setup your browser
  - Run the server with `python src/proxy.py` and note down the address outputted.
  - Update your browser to use an HTTP proxy using the address you noted down.
- Run the server
- Make a request to an HTTP site, I use [GAIA EDU](http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file1.html)
- Note in the logs and in your `cache` folder that a new file has been created with the response received by the proxy server.
- Clear your browser's cache.
- Navigate to the same URL and now note in the logs that you can see 'Read from cache'. This means the server picked up the file from the cache, saving you time!

---

## Passing Criteria

1. The proxy server can accept a request and forward the request to the destination server
2. The proxy server can take the response and map it to the browser.
3. Threading allows simultaneous requests to be made by the browser.

---

## Future Development

- Clean up code. Style is not clean or consistent. Hacked my way to get a working version.
- Add in timing.
  - Record the amount of time it took for a request that doesn't have a cache hit.
  - Report the amount of time saved when you do have a cache hit.

---
