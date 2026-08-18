#!/usr/bin/env python3
"""Wrap the board fragment (body.html) in a full HTML document -> index.html.

The artifact runtime supplies <head> automatically; GitHub Pages does not.
Run after copying the current board to body.html.
"""
import pathlib

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3E%3Ctext y=%2714%27 font-size=%2714%27%3E%F0%9F%8E%BE%3C/text%3E%3C/svg%3E">
<style>*,*::before,*::after{box-sizing:border-box}body{margin:0}</style>
</head>
<body>
"""

here = pathlib.Path(__file__).parent
body = (here / "body.html").read_text(encoding="utf-8")
(here / "index.html").write_text(HEAD + body + "\n</body>\n</html>\n", encoding="utf-8")
print("index.html written:", (here / "index.html").stat().st_size, "bytes")
