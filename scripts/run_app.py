from __future__ import annotations
import argparse
from app.commands import feed, status

def main():
    parser = argparse.ArgumentParser(description="IoT Cat Feeder App (publisher)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_feed = sub.add_parser("feed", help="Dispense food in grams")
    p_feed.add_argument("grams", type=int, help="Amount in grams, e.g., 50")

    sub.add_parser("status", help="Ask device for status")

    args = parser.parse_args()
    if args.cmd == "feed":
        feed(args.grams)
        print(f"[App] Sent FEED {args.grams}")
    elif args.cmd == "status":
        status()
        print("[App] Sent STATUS?")

if __name__ == "__main__":
    main()
