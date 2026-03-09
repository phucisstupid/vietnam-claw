# openclaw-vn-commerce

A Vietnam-focused OpenClaw commerce plugin pack.

## Vision

Bring genuinely useful Vietnam-native workflows into OpenClaw:

- VietQR payment QR generation
- Shopee product checking
- Lazada product checking
- price comparison
- deal tracking
- shop trust quick scans

## Why this exists

Most assistant/plugin ecosystems feel generic and Western-first. This project is meant to be practical for Vietnamese users and small businesses.

## MVP

### 1. VietQR generator
- build VietQR image URLs from bank + account + amount + transfer note
- output raw URL or markdown preview

### 2. Shopee checker
- accept product URL
- extract core product/shop information

### 3. Lazada checker
- accept product URL
- extract core product/shop information

## Repo structure

```text
plugins/
  vietqr/
  shopee/
  lazada/
shared/
docs/
examples/
```

## Current status

- [x] project scaffold
- [x] VietQR module v0
- [ ] VietQR OpenClaw skill/plugin wrapper
- [ ] Shopee checker
- [ ] Lazada checker
- [ ] compare command

## Quick start

```bash
python3 plugins/vietqr/vietqr.py --bank MBBank --account 0123456789 --amount 50000 --note "cafe"
```

## Example output

```text
https://img.vietqr.io/image/MBBank-0123456789-compact2.png?amount=50000&addInfo=cafe
```

## Notes

This project starts with public/open endpoints where possible. Marketplace integrations may require careful scraping, caching, and rate limiting.
