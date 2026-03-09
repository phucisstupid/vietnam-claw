#!/usr/bin/env python3
from __future__ import annotations

import argparse
from urllib.parse import urlencode, quote

BASE_URL = "https://img.vietqr.io/image"


def build_vietqr_url(
    bank: str,
    account: str,
    amount: int | None = None,
    note: str | None = None,
    account_name: str | None = None,
    template: str = "compact2",
) -> str:
    bank = bank.strip()
    account = account.strip()
    path = f"{BASE_URL}/{quote(bank)}-{quote(account)}-{quote(template)}.png"

    params: dict[str, str] = {}
    if amount is not None:
        params["amount"] = str(amount)
    if note:
        params["addInfo"] = note
    if account_name:
        params["accountName"] = account_name

    if not params:
        return path
    return f"{path}?{urlencode(params)}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate VietQR image URLs.")
    parser.add_argument("--bank", required=True, help="Bank code or bank name alias, e.g. MBBank")
    parser.add_argument("--account", required=True, help="Bank account number")
    parser.add_argument("--amount", type=int, default=None, help="Transfer amount")
    parser.add_argument("--note", default=None, help="Transfer note / addInfo")
    parser.add_argument("--account-name", default=None, help="Account holder name")
    parser.add_argument("--template", default="compact2", help="QR template, e.g. compact2")
    parser.add_argument("--markdown", action="store_true", help="Print markdown image preview")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    url = build_vietqr_url(
        bank=args.bank,
        account=args.account,
        amount=args.amount,
        note=args.note,
        account_name=args.account_name,
        template=args.template,
    )
    if args.markdown:
        print(f"![VietQR]({url})")
    else:
        print(url)


if __name__ == "__main__":
    main()
