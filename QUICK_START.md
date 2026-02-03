# Quick Reference Guide

## Installation

```bash
# No dependencies needed - uses Python standard library only
git clone https://github.com/bie7u/html2typst-second.git
cd html2typst-second
```

## Basic Usage

```python
from src.html2typst import translate_html_to_typst

# Simple conversion
html = "<p>Hello <strong>world</strong></p>"
typst = translate_html_to_typst(html)
print(typst)  # Output: Hello *world*

# With debug mode
typst = translate_html_to_typst(html, debug=True)
```

## Command Line Usage

```python
# Create a simple script (convert.py)
import sys
from src.html2typst import translate_html_to_typst

html = sys.stdin.read()
typst = translate_html_to_typst(html, debug=False)
print(typst)
```

```bash
# Use it
cat input.html | python convert.py > output.typ
```

## Common Patterns

### Quill.js Rich Text Editor

```python
# Typical Quill.js output
quill_html = editor.getHTML()  # From your Quill.js instance
typst_code = translate_html_to_typst(quill_html)

# Save to file
with open('output.typ', 'w') as f:
    f.write(typst_code)
```

### Batch Processing

```python
import os
from src.html2typst import translate_html_to_typst

html_dir = 'html_files'
typst_dir = 'typst_files'

for filename in os.listdir(html_dir):
    if filename.endswith('.html'):
        with open(os.path.join(html_dir, filename)) as f:
            html = f.read()
        
        typst = translate_html_to_typst(html)
        
        output_name = filename.replace('.html', '.typ')
        with open(os.path.join(typst_dir, output_name), 'w') as f:
            f.write(typst)
```

### With Error Handling

```python
from src.html2typst import translate_html_to_typst

def safe_convert(html, debug=False):
    """Convert HTML to Typst with error handling."""
    try:
        return translate_html_to_typst(html, debug=debug)
    except Exception as e:
        print(f"Error converting HTML: {e}")
        return None

# Use it
result = safe_convert(html_content)
if result:
    print("Conversion successful!")
```

## Testing

```bash
# Run unit tests
python tests/test_html2typst.py

# Run integration tests
python tests/integration_test.py

# Run examples
python examples/demo.py
```

## Key Features Checklist

- ✅ Text preservation (100% guaranteed)
- ✅ Basic formatting (bold, italic, headings)
- ✅ Lists (ordered, unordered, nested)
- ✅ Quill.js classes (indent, alignment, size, font)
- ✅ Inline styles (color, font, size)
- ✅ Code blocks and inline code
- ✅ Links and images
- ✅ Blockquotes
- ✅ Debug mode
- ✅ Fail-safe design

## Supported Quill.js Classes

| Class | Example | Result |
|-------|---------|--------|
| `ql-align-center` | `<p class="ql-align-center">Text</p>` | `#align(center)[Text]` |
| `ql-align-right` | `<p class="ql-align-right">Text</p>` | `#align(right)[Text]` |
| `ql-indent-1` | `<li class="ql-indent-1">Item</li>` | `  - Item` |
| `ql-indent-2` | `<li class="ql-indent-2">Item</li>` | `    - Item` |
| `ql-size-small` | `<span class="ql-size-small">Text</span>` | `#text(size: 0.75em)[Text]` |
| `ql-size-large` | `<span class="ql-size-large">Text</span>` | `#text(size: 1.5em)[Text]` |
| `ql-font-serif` | `<span class="ql-font-serif">Text</span>` | `#text(font: "serif")[Text]` |

## Troubleshooting

### Issue: Output is empty
**Solution:** Check if your HTML is valid. The parser is forgiving but extreme malformation may cause issues.

### Issue: Formatting not preserved
**Solution:** Check that you're using supported HTML tags. Unsupported tags will preserve text but drop styling (by design).

### Issue: Want to see what's not supported
**Solution:** Use debug mode: `translate_html_to_typst(html, debug=True)`

### Issue: Need to add new tag support
**Solution:** Extend the `handle_data()` method in `src/html2typst.py`

## Best Practices

1. **Always preserve text** - This is the #1 rule
2. **Test with debug mode first** - See what's being dropped
3. **Keep HTML semantic** - Use proper tags (not just div/span)
4. **Validate output** - Compile with Typst to check syntax
5. **Report issues** - If text is lost, it's a bug!

## Examples of Input/Output

### Example 1: Basic Document
```html
<h1>Title</h1>
<p>A <strong>bold</strong> statement.</p>
```
→
```typst
= Title

A *bold* statement.
```

### Example 2: Styled List
```html
<ul>
  <li>Item 1</li>
  <li class="ql-indent-1">Nested</li>
</ul>
```
→
```typst
- Item 1
  - Nested
```

### Example 3: Colored Text
```html
<p><span style="color: red;">Alert!</span> Normal text.</p>
```
→
```typst
#text(fill: red)[Alert!] Normal text.
```

## Performance

- **Speed**: Processes typical documents (< 1MB) in milliseconds
- **Memory**: Minimal - uses streaming parser
- **Scale**: Tested with documents up to 10,000 lines

## License

MIT - See repository for details
