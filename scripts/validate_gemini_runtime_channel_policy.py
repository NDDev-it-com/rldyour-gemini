#!/usr/bin/env python3
from gemini_contract import main

if __name__ == "__main__":
    raise SystemExit(main(["runtime-channel", *(__import__("sys").argv[1:])]))
