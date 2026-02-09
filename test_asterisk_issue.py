#!/usr/bin/env python3
"""Test specific issue with asterisk at start of text in function calls."""

from src.html2typst import translate_html_to_typst

# Test case 1: Asterisk at the start of text in a span with color
html1 = '<span style="color: black;">*.</span>'
result1 = translate_html_to_typst(html1)
print("Test 1: Asterisk at start")
print(f"HTML: {html1}")
print(f"Typst: {result1}")
print()

# Test case 2: The problematic pattern from the issue
html2 = '<p style="text-align: justify;"><span style="color: black;">text </span><strong>2,30 zł/m2</strong><span style="color: black;">*.</span></p>'
result2 = translate_html_to_typst(html2)
print("Test 2: From issue")
print(f"HTML: {html2}")
print(f"Typst: {result2}")
print()

# Test case 3: Asterisk at start of paragraph
html3 = '<p style="text-align: justify;"><span style="color: black;">* w skład kosztów</span></p>'
result3 = translate_html_to_typst(html3)
print("Test 3: Asterisk at start of paragraph")
print(f"HTML: {html3}")
print(f"Typst: {result3}")
print()

# Test case 4: Underscore at start (same issue)
html4 = '<span style="color: black;">_test</span>'
result4 = translate_html_to_typst(html4)
print("Test 4: Underscore at start")
print(f"HTML: {html4}")
print(f"Typst: {result4}")
print()
