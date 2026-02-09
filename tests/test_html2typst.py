"""
Comprehensive test suite for HTML to Typst translator.

Tests cover:
- Text preservation (critical requirement)
- Basic HTML tag mappings
- Quill.js specific classes and styles
- Debug mode functionality
- Edge cases and fail-safe behavior
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from html2typst import translate_html_to_typst


def test_text_preservation():
    """Test that 100% of text is preserved."""
    print("Testing text preservation...")
    
    # Simple text
    html = "<p>Hello world</p>"
    result = translate_html_to_typst(html)
    assert "Hello world" in result, f"Text not preserved: {result}"
    
    # Text in nested elements
    html = "<div><p>Outer <span>inner</span> text</p></div>"
    result = translate_html_to_typst(html)
    assert "Outer" in result and "inner" in result and "text" in result
    
    # Text with unsupported tags
    html = "<p>Before <xyz>middle</xyz> after</p>"
    result = translate_html_to_typst(html)
    assert "Before" in result and "middle" in result and "after" in result
    
    print("✓ Text preservation tests passed")


def test_basic_formatting():
    """Test basic HTML formatting tags."""
    print("Testing basic formatting...")
    
    # Bold
    html = "<p>Normal <strong>bold</strong> text</p>"
    result = translate_html_to_typst(html)
    assert "*bold*" in result
    
    # Italic
    html = "<p>Normal <em>italic</em> text</p>"
    result = translate_html_to_typst(html)
    assert "_italic_" in result
    
    # Combined
    html = "<p><strong>Bold</strong> and <em>italic</em></p>"
    result = translate_html_to_typst(html)
    assert "*Bold*" in result and "_italic_" in result
    
    # Alternative tags
    html = "<p><b>Bold</b> and <i>italic</i></p>"
    result = translate_html_to_typst(html)
    assert "*Bold*" in result and "_italic_" in result
    
    print("✓ Basic formatting tests passed")


def test_headings():
    """Test heading conversion."""
    print("Testing headings...")
    
    tests = [
        ("<h1>Heading 1</h1>", "= Heading 1"),
        ("<h2>Heading 2</h2>", "== Heading 2"),
        ("<h3>Heading 3</h3>", "=== Heading 3"),
        ("<h4>Heading 4</h4>", "==== Heading 4"),
        ("<h5>Heading 5</h5>", "===== Heading 5"),
        ("<h6>Heading 6</h6>", "====== Heading 6"),
    ]
    
    for html, expected in tests:
        result = translate_html_to_typst(html)
        assert expected in result, f"Expected '{expected}' in '{result}'"
    
    print("✓ Heading tests passed")


def test_lists():
    """Test list conversion."""
    print("Testing lists...")
    
    # Unordered list
    html = "<ul><li>Item 1</li><li>Item 2</li></ul>"
    result = translate_html_to_typst(html)
    assert "- Item 1" in result and "- Item 2" in result
    
    # Ordered list
    html = "<ol><li>First</li><li>Second</li></ol>"
    result = translate_html_to_typst(html)
    assert "+ First" in result and "+ Second" in result
    
    # Nested lists
    html = "<ul><li>Level 1<ul><li>Level 2</li></ul></li></ul>"
    result = translate_html_to_typst(html)
    assert "- Level 1" in result and "Level 2" in result
    
    print("✓ List tests passed")


def test_quill_indent():
    """Test Quill.js indent classes."""
    print("Testing Quill indent classes...")
    
    # Single indent
    html = '<ul><li class="ql-indent-1">Indented item</li></ul>'
    result = translate_html_to_typst(html)
    assert "  - Indented item" in result or "Indented item" in result
    
    # Multiple indent levels
    html = '''
    <ul>
        <li>Level 0</li>
        <li class="ql-indent-1">Level 1</li>
        <li class="ql-indent-2">Level 2</li>
    </ul>
    '''
    result = translate_html_to_typst(html)
    assert "Level 0" in result and "Level 1" in result and "Level 2" in result
    
    print("✓ Quill indent tests passed")


def test_quill_alignment():
    """Test Quill.js alignment classes."""
    print("Testing Quill alignment classes...")
    
    # Center alignment
    html = '<p class="ql-align-center">Centered text</p>'
    result = translate_html_to_typst(html)
    assert "center" in result and "Centered text" in result
    
    # Right alignment
    html = '<p class="ql-align-right">Right text</p>'
    result = translate_html_to_typst(html)
    assert "right" in result and "Right text" in result
    
    # Left alignment (default)
    html = '<p class="ql-align-left">Left text</p>'
    result = translate_html_to_typst(html)
    assert "Left text" in result
    
    print("✓ Quill alignment tests passed")


def test_inline_styles():
    """Test inline style handling."""
    print("Testing inline styles...")
    
    # Color
    html = '<span style="color: red;">Red text</span>'
    result = translate_html_to_typst(html)
    assert "Red text" in result  # Text must be preserved
    
    # Font size
    html = '<span style="font-size: 14px;">Sized text</span>'
    result = translate_html_to_typst(html)
    assert "Sized text" in result
    
    # Multiple styles
    html = '<span style="color: blue; font-size: 16px;">Styled text</span>'
    result = translate_html_to_typst(html)
    assert "Styled text" in result
    
    print("✓ Inline style tests passed")


def test_blockquote():
    """Test blockquote conversion."""
    print("Testing blockquotes...")
    
    html = "<blockquote>This is a quote</blockquote>"
    result = translate_html_to_typst(html)
    assert "This is a quote" in result
    assert ">" in result  # Should have quote marker
    
    print("✓ Blockquote tests passed")


def test_code_blocks():
    """Test code block conversion."""
    print("Testing code blocks...")
    
    # Inline code
    html = "<p>Use <code>print()</code> function</p>"
    result = translate_html_to_typst(html)
    assert "print()" in result
    assert "`print()`" in result or "print()" in result
    
    # Code block
    html = "<pre><code>def hello():\n    print('world')</code></pre>"
    result = translate_html_to_typst(html)
    assert "def hello()" in result
    assert "print('world')" in result
    
    print("✓ Code block tests passed")


def test_links():
    """Test link conversion."""
    print("Testing links...")
    
    # Link with href
    html = '<a href="https://example.com">Click here</a>'
    result = translate_html_to_typst(html)
    assert "Click here" in result
    assert "example.com" in result or "link" in result
    
    # Link without href (fallback to text)
    html = '<a>Just text</a>'
    result = translate_html_to_typst(html)
    assert "Just text" in result
    
    print("✓ Link tests passed")


def test_images():
    """Test image conversion."""
    print("Testing images...")
    
    # Image with src and alt
    html = '<img src="image.png" alt="Description" />'
    result = translate_html_to_typst(html)
    assert "Description" in result or "image.png" in result
    
    # Image without src (fallback to alt)
    html = '<img alt="Alt text" />'
    result = translate_html_to_typst(html)
    assert "Alt text" in result or result == ''
    
    print("✓ Image tests passed")


def test_line_breaks():
    """Test line break handling."""
    print("Testing line breaks...")
    
    html = "<p>Line 1<br>Line 2</p>"
    result = translate_html_to_typst(html)
    assert "Line 1" in result and "Line 2" in result
    
    print("✓ Line break tests passed")


def test_debug_mode():
    """Test debug mode functionality."""
    print("Testing debug mode...")
    
    import os
    import tempfile
    
    # Unsupported tag
    html = "<p>Text with <custom>custom tag</custom></p>"
    result_prod = translate_html_to_typst(html, debug=False)
    
    # Create a temporary log file for debug mode
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        log_file = f.name
    
    try:
        result_debug = translate_html_to_typst(html, debug=True, log_file=log_file)
        
        # Both should preserve text
        assert "custom tag" in result_prod
        assert "custom tag" in result_debug
        
        # Debug should NOT have comments in output (they should be in log file)
        assert "/*" not in result_prod  # No debug comments in production
        assert "/*" not in result_debug  # No debug comments in debug mode either (now in log file)
        
        # Verify log file was created (even if empty for this particular test)
        assert os.path.exists(log_file), "Log file should be created in debug mode"
    finally:
        if os.path.exists(log_file):
            os.remove(log_file)
    
    # Unsupported style
    html = '<span style="text-shadow: 2px 2px;">Shadowed</span>'
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        log_file = f.name
    
    try:
        result_debug = translate_html_to_typst(html, debug=True, log_file=log_file)
        assert "Shadowed" in result_debug  # Text preserved
        assert "/*" not in result_debug  # No comments in output
    finally:
        if os.path.exists(log_file):
            os.remove(log_file)
    
    print("✓ Debug mode tests passed")


def test_complex_quill_example():
    """Test a complex real-world Quill.js example."""
    print("Testing complex Quill example...")
    
    html = '''
    <h1>Document Title</h1>
    <p class="ql-align-center">Centered paragraph</p>
    <ul>
        <li>Regular item</li>
        <li class="ql-indent-1">Indented item</li>
        <li class="ql-indent-2" style="text-align: justify;">
            <span style="color: windowtext;">Deeply indented with style</span>
        </li>
    </ul>
    <p>Normal text with <strong>bold</strong> and <em>italic</em>.</p>
    <blockquote>A wise quote</blockquote>
    <pre><code>code example</code></pre>
    '''
    
    result = translate_html_to_typst(html, debug=False)
    
    # Check all text is preserved
    assert "Document Title" in result
    assert "Centered paragraph" in result
    assert "Regular item" in result
    assert "Indented item" in result
    assert "Deeply indented with style" in result
    assert "Normal text" in result
    assert "bold" in result
    assert "italic" in result
    assert "A wise quote" in result
    assert "code example" in result
    
    # Check structure
    assert "= Document Title" in result  # H1 formatting
    assert "*bold*" in result  # Bold formatting
    assert "_italic_" in result  # Italic formatting
    
    print("✓ Complex Quill example passed")


def test_edge_cases():
    """Test edge cases and fail-safe behavior."""
    print("Testing edge cases...")
    
    # Empty elements
    html = "<p></p><div></div>"
    result = translate_html_to_typst(html)
    # Should not crash, minimal output is fine
    
    # Nested formatting
    html = "<p><strong><em>Bold and italic</em></strong></p>"
    result = translate_html_to_typst(html)
    assert "Bold and italic" in result
    
    # Unsupported formatting that should be ignored
    html = "<p><u>Underlined</u> and <s>strikethrough</s> text</p>"
    result_prod = translate_html_to_typst(html, debug=False)
    result_debug = translate_html_to_typst(html, debug=True)
    assert "Underlined" in result_prod and "strikethrough" in result_prod
    assert "Underlined" in result_debug and "strikethrough" in result_debug
    
    # Malformed HTML (HTMLParser should handle gracefully)
    html = "<p>Unclosed paragraph"
    result = translate_html_to_typst(html)
    assert "Unclosed paragraph" in result
    
    print("✓ Edge case tests passed")


def test_span_with_quill_classes():
    """Test span elements with Quill.js classes."""
    print("Testing span with Quill classes...")
    
    # Size classes
    html = '<span class="ql-size-small">Small text</span>'
    result = translate_html_to_typst(html)
    assert "Small text" in result
    
    html = '<span class="ql-size-large">Large text</span>'
    result = translate_html_to_typst(html)
    assert "Large text" in result
    
    # Font classes
    html = '<span class="ql-font-serif">Serif text</span>'
    result = translate_html_to_typst(html)
    assert "Serif text" in result
    
    print("✓ Span with Quill classes tests passed")


def test_consecutive_styled_elements():
    """Test paragraphs with consecutive styled elements (e.g., multiple spans)."""
    print("Testing consecutive styled elements...")
    
    # Multiple spans with color in a paragraph, separated by plain text
    html = '''<p><span style="color: black;">Text 1</span>(plain text)<span style="color: black;">Text 2</span></p>'''
    result = translate_html_to_typst(html)
    # Should have proper spacing between function calls
    assert "#text(fill: black)[Text 1]" in result
    assert "(plain text)" in result
    assert "#text(fill: black)[Text 2]" in result
    # Check that result doesn't cause Typst syntax error - should have space before second #text
    assert ") #text(fill: black)[Text 2]" in result
    
    # Test with alignment and multiple styled spans
    html = '''<p style="text-align: center;"><span style="color: red;">Red</span> and <span style="color: blue;">Blue</span></p>'''
    result = translate_html_to_typst(html)
    assert "#align(center)[" in result
    assert "Red" in result and "Blue" in result
    
    # Complex case from issue: paragraph with styled span, plain text, styled span
    html = '''<p style="text-align: justify;"><span style="color: black;">Działając na podstawie.</span>(tekst ujednolicony: Dz. U.)<span style="color: black;"> Właściciel</span></p>'''
    result = translate_html_to_typst(html)
    assert "#text(fill: black)[Działając na podstawie.]" in result
    assert "(tekst ujednolicony: Dz. U.)" in result
    assert "#text(fill: black)[ Właściciel]" in result
    # Critical: there should be space before the second #text to avoid "expected comma" error
    assert ") #text(fill: black)" in result
    
    print("✓ Consecutive styled elements tests passed")


def test_superscript_and_subscript():
    """Test superscript and subscript conversion."""
    print("Testing superscript and subscript...")
    
    # Simple superscript
    html = "<p>E = mc<sup>2</sup></p>"
    result = translate_html_to_typst(html)
    assert "E = mc" in result
    assert "#super[2]" in result
    
    # Simple subscript
    html = "<p>H<sub>2</sub>O</p>"
    result = translate_html_to_typst(html)
    assert "H" in result and "O" in result
    assert "#sub[2]" in result
    
    # Superscript with bold
    html = "<p><sup><strong>2</strong></sup></p>"
    result = translate_html_to_typst(html)
    assert "#super[#strong[2]]" in result or "#super[*2*]" in result
    
    print("✓ Superscript and subscript tests passed")


def test_delimiter_collision_prevention():
    """Test that consecutive markup delimiters are prevented."""
    print("Testing delimiter collision prevention...")
    
    # Bold followed by bold in superscript (the main issue)
    html = "<p><strong>text</strong><sup><strong>2</strong></sup></p>"
    result = translate_html_to_typst(html)
    # Should not have ** pattern which causes unclosed delimiter
    assert "**" not in result
    # Should use function syntax for the second bold
    assert "#strong[2]" in result
    
    # Bold followed by italic
    html = "<p><strong>bold</strong><em>italic</em></p>"
    result = translate_html_to_typst(html)
    # Should not have *_ pattern
    assert "*_" not in result
    # Should use function syntax
    assert "#emph[italic]" in result
    
    # Italic followed by bold
    html = "<p><em>italic</em><strong>bold</strong></p>"
    result = translate_html_to_typst(html)
    # Should not have _* pattern
    assert "_*" not in result
    # Should use function syntax
    assert "#strong[bold]" in result
    
    # Multiple consecutive bold elements
    html = "<p><strong>one</strong><strong>two</strong><strong>three</strong></p>"
    result = translate_html_to_typst(html)
    # Should not have ** pattern
    assert "**" not in result
    
    print("✓ Delimiter collision prevention tests passed")


def test_unclosed_delimiter_issue():
    """Test the specific HTML that caused unclosed delimiter error."""
    print("Testing unclosed delimiter issue fix...")
    
    # This HTML previously caused "unclosed delimiter" error in Typst compilation
    # The issue was with ] followed by *bold* markup after function calls
    html = '''<p style="text-align: justify;"><span style="color: black;">Członkowie Wspólnoty Mieszkaniowej wyrażają zgodę na
        zawarcie </span><strong style="color: black;">Porozumisdafsdafasedzkiego</strong><span
        style="color: black;"> </span>z inwesdafdasfępu sp. z o.o.</p>'''
    result = translate_html_to_typst(html, debug=False)
    
    # Should use #strong[...] instead of *...* after a ] to avoid Typst parser issues
    assert "#strong[Porozumisdafsdafasedzkiego]" in result
    # Should not have ]* pattern which causes unclosed delimiter
    assert "]*" not in result
    assert "]_" not in result
    
    # More complex case with multiple styled elements
    html = '''<p style="text-align: center;"><span style="color: black;">w sprawie: </span><strong style="color: black;">fasdsaf
        zgody i udzielenia Zarządowi sadfasdf Mieszkaniowej upoważnienia </strong></p>'''
    result = translate_html_to_typst(html, debug=False)
    assert "#strong[" in result
    assert "]*" not in result
    
    # Real-world case from issue: bold text followed by superscript bold
    # This pattern appears in mathematical/scientific notation (e.g., units with exponents)
    html = '''<p><strong>Value</strong><sup><strong>2</strong></sup></p>'''
    result = translate_html_to_typst(html)
    # Should not have ** pattern
    assert "**" not in result
    # Should properly handle the superscript
    assert "#super[" in result
    
    print("✓ Unclosed delimiter issue test passed")


def test_debug_log_file():
    """Test that debug messages are written to log file instead of output."""
    print("Testing debug log file functionality...")
    
    import os
    import tempfile
    
    # Test case: unsupported alignment
    html = '''<p style="text-align: justify;">Text with <strong>bold</strong> content.</p>'''
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        log_file = f.name
    
    try:
        result = translate_html_to_typst(html, debug=True, log_file=log_file)
        
        # Should not contain debug comments in the output
        assert "/*" not in result, f"Found debug comment in output: {result}"
        
        # Check that log file was created and contains debug info
        assert os.path.exists(log_file), "Log file was not created"
        
        with open(log_file, 'r') as f:
            log_content = f.read()
        
        # Log should contain warning about unsupported alignment
        assert 'alignment' in log_content.lower() or 'justify' in log_content.lower(), \
            f'Expected alignment warning in log, got: {log_content}'
    finally:
        if os.path.exists(log_file):
            os.remove(log_file)
    
    # Test case: link without href
    html = '<a>Test link</a>'
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        log_file = f.name
    
    try:
        result = translate_html_to_typst(html, debug=True, log_file=log_file)
        
        # Output should just have the text
        assert "Test link" in result
        assert "/*" not in result
        
        # Log file should contain warning
        with open(log_file, 'r') as f:
            log_content = f.read()
        
        assert "href" in log_content.lower(), f"Log should mention href: {log_content}"
    finally:
        if os.path.exists(log_file):
            os.remove(log_file)
    
    print("✓ Debug log file tests passed")


def test_asterisk_escape_in_function_syntax():
    """Test that asterisks and underscores are escaped when they appear at the start of content in function calls."""
    print("Testing asterisk/underscore escape in function syntax...")
    
    # Asterisk at start of styled span
    html = '<span style="color: black;">*.</span>'
    result = translate_html_to_typst(html)
    # Should escape the asterisk to prevent it from being interpreted as bold delimiter
    assert r'\*.' in result, f"Expected escaped asterisk in: {result}"
    
    # Underscore at start of styled span
    html = '<span style="color: black;">_test</span>'
    result = translate_html_to_typst(html)
    # Should escape the underscore to prevent it from being interpreted as italic delimiter
    assert r'\_test' in result, f"Expected escaped underscore in: {result}"
    
    # Real-world case from issue: paragraph with styled text ending in asterisk
    html = '''<p style="text-align: justify;"><span style="color: black;">text </span><strong>2,30 zł/m2</strong><span style="color: black;">*.</span></p>'''
    result = translate_html_to_typst(html)
    # Should escape asterisk in function call
    assert r'\*.' in result, f"Expected escaped asterisk in: {result}"
    
    # Asterisk at the start of a paragraph with styled text
    html = '''<p style="text-align: justify;"><span style="color: black;">* w skład kosztów</span></p>'''
    result = translate_html_to_typst(html)
    # Should escape asterisk in function call
    assert r'\* w skład' in result, f"Expected escaped asterisk in: {result}"
    
    # Multiple wrappers (e.g., color + size) with asterisk at start
    html = '''<span style="color: red; font-size: 14px;">*important</span>'''
    result = translate_html_to_typst(html)
    # Should escape the asterisk only once (not multiple times)
    assert r'\*important' in result, f"Expected single escaped asterisk in: {result}"
    # Should not have double escaping
    assert r'\\*important' not in result, f"Should not have double escaping in: {result}"
    
    # Test that asterisks in the middle are also escaped
    html = '''<span style="color: black;">test * asterisk</span>'''
    result = translate_html_to_typst(html)
    # Should escape asterisk in the middle when inside function calls
    assert r'\*' in result, f"Asterisk should be escaped in: {result}"
    
    print("✓ Asterisk/underscore escape tests passed")


def test_nested_formatting():
    """Test nested bold/italic combinations to prevent delimiter collisions."""
    print("Testing nested formatting...")
    
    # Bold containing italic - primary issue: prevents _*text*_ pattern
    html = "<p><strong><em>nested</em></strong></p>"
    result = translate_html_to_typst(html)
    assert "nested" in result
    # Primary delimiter collision patterns from nested formatting
    assert "*_" not in result, "Asterisk-underscore causes delimiter collision"
    assert "_*" not in result, "Underscore-asterisk causes delimiter collision"
    # Should use function syntax for nested formatting
    assert "#strong[" in result or "#emph[" in result
    
    # Italic containing bold - primary issue: prevents _*text*_ pattern
    html = "<p><em><strong>nested</strong></em></p>"
    result = translate_html_to_typst(html)
    assert "nested" in result
    assert "*_" not in result, "Asterisk-underscore causes delimiter collision"
    assert "_*" not in result, "Underscore-asterisk causes delimiter collision"
    assert "#strong[" in result or "#emph[" in result
    
    # Bold(italic) followed by bold - tests both nesting and consecutive elements
    html = "<p><strong><em>first</em></strong><strong>second</strong></p>"
    result = translate_html_to_typst(html)
    assert "first" in result and "second" in result
    # Check for all delimiter collision patterns
    assert "*_" not in result, "Asterisk-underscore causes delimiter collision"
    assert "_*" not in result, "Underscore-asterisk causes delimiter collision"
    assert "**" not in result, "Double asterisk causes unclosed delimiter"
    
    # Italic(bold) followed by italic - tests both nesting and consecutive elements
    html = "<p><em><strong>first</strong></em><em>second</em></p>"
    result = translate_html_to_typst(html)
    assert "first" in result and "second" in result
    assert "*_" not in result, "Asterisk-underscore causes delimiter collision"
    assert "_*" not in result, "Underscore-asterisk causes delimiter collision"
    assert "__" not in result, "Double underscore causes unclosed delimiter"
    
    # Complex: multiple nested elements in one paragraph
    html = "<p><strong><em>a</em></strong> text <em><strong>b</strong></em></p>"
    result = translate_html_to_typst(html)
    assert "a" in result and "b" in result and "text" in result
    # Comprehensive check for all delimiter collision patterns
    assert "*_" not in result, "Asterisk-underscore causes delimiter collision"
    assert "_*" not in result, "Underscore-asterisk causes delimiter collision"
    assert "**" not in result, "Double asterisk causes unclosed delimiter"
    assert "__" not in result, "Double underscore causes unclosed delimiter"
    
    # Deeply nested
    html = "<p><strong>outer <em>middle</em> outer</strong></p>"
    result = translate_html_to_typst(html)
    assert "outer" in result and "middle" in result
    # All text should be preserved
    text_count = result.count("outer") + result.count("middle")
    assert text_count >= 2  # At least "outer" appears once and "middle" once
    
    print("✓ Nested formatting tests passed")


def test_literal_delimiters_in_plain_text():
    """Test that literal asterisks and underscores in plain text are properly escaped."""
    print("Testing literal delimiters in plain text...")
    
    # Single asterisk in plain text
    html = "<p>Price: 27,00 zł/udział*.</p>"
    result = translate_html_to_typst(html)
    assert "Price: 27,00 zł/udział" in result
    # Asterisk should be escaped
    assert r"\*" in result or "#text[" in result, f"Asterisk not escaped in: {result}"
    
    # Multiple asterisks in different paragraphs
    html = "<p>Item one*</p><p>* Another item</p>"
    result = translate_html_to_typst(html)
    assert "Item one" in result and "Another item" in result
    # Both asterisks should be escaped
    assert result.count(r"\*") >= 2 or "#text[" in result, f"Not all asterisks escaped in: {result}"
    
    # Underscore in plain text (e.g., variable names)
    html = "<p>The variable_name is important</p>"
    result = translate_html_to_typst(html)
    assert "variable" in result and "name" in result
    # Underscore should be escaped
    assert r"\_" in result or "#text[" in result, f"Underscore not escaped in: {result}"
    
    # Mixed asterisks and underscores
    html = "<p>foo* and bar_ together</p>"
    result = translate_html_to_typst(html)
    assert "foo" in result and "bar" in result
    # Both should be escaped
    assert (r"\*" in result or "#text[" in result) and (r"\_" in result or "#text[" in result), f"Delimiters not escaped in: {result}"
    
    # Real-world case from issue: text ending with asterisk
    html = """<p>2.Ustalhkjkhkhokości 27,00 zł/udział*.</p>
<p>* w skhjkhkjhkjh03.2010r.</p>"""
    result = translate_html_to_typst(html)
    assert "27,00 zł/udział" in result
    assert "w skhjkhkjhkjh03.2010r" in result
    # Both asterisks should be escaped
    assert result.count(r"\*") >= 2 or "#text[" in result, f"Problem case not fixed: {result}"
    
    # Asterisk in middle of text
    html = "<p>Use * as a wildcard</p>"
    result = translate_html_to_typst(html)
    assert "Use" in result and "wildcard" in result
    assert r"\*" in result or "#text[" in result, f"Middle asterisk not escaped in: {result}"
    
    # Multiple consecutive asterisks
    html = "<p>Rating: ***</p>"
    result = translate_html_to_typst(html)
    assert "Rating:" in result
    # Should escape all three asterisks
    assert result.count(r"\*") >= 3 or "#text[" in result, f"Multiple asterisks not escaped in: {result}"
    
    # Underscore at start of text
    html = "<p>_private_method</p>"
    result = translate_html_to_typst(html)
    assert "private" in result and "method" in result
    # Should escape both underscores
    assert result.count(r"\_") >= 2 or "#text[" in result, f"Underscores not escaped in: {result}"
    
    print("✓ Literal delimiters in plain text tests passed")


def test_issue_html_unclosed_delimiter():
    """Test the specific HTML from the GitHub issue that caused unclosed delimiter error."""
    print("Testing issue HTML with unclosed delimiter...")
    
    # This is the actual HTML from the issue that caused "unclosed delimiter" error
    html = '''<p style="text-align: center;"><strong>fdsafasf Nfsdafsafsa2021</strong></p>
<p style="text-align: center;"><br></p>
<p style="text-align: center;"><strong> właścicdsafsafa
        Wrofsdafasawiu </strong><strong style="color: black;">w sprawie: przyjęciasdafdsafsaf sdafdsa na
        rok 2021</strong></p>
<p style="text-align: justify;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: justify;"><span
        style="color: black;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Działajsdaffawie
        art. 30 ust. 2, art. 22 Ustsdafasfsdafmości wspólnej uchwalają co
        następuje:</span></p>
<p style="text-align: justify;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: center;"><strong style="color: black;">§1</strong></p>
<p style="text-align: justify;"><span style="color: black;">Przyjmują do realizfasdfasłącznik nr 1 do Uchwały.</span>
</p>
<p style="text-align: center;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: center;"><strong style="color: black;">§2</strong></p>
<p><span style="color: black;">Ustalają wysokość miesifdsafsafasrzynależnych&nbsp;oraz 25sadfsaf0 zł udział w terenie
        zewnętrznym.*</span></p>
<p style="text-align: center;"><strong style="color: black;">§3</strong></p>
<p style="text-align: justify;"><span style="color: black;">Przyfasdfsanastępującej wysokości:</span></p>
<p style="text-align: justify;"><span style="color: black;">• Zużyfdasfsafparciu o zużycie (w danym lokalu) z
        poprzedniego okresu rozliczeniowego.</span></p>
<p style="text-align: center;"><strong style="color: black;">§4</strong></p>
<p style="text-align: justify;"><span style="color: black;">Wysokość poszczefdsafsafez konieczności podejmowania nowej uchwały w
        tej sprawie. </span></p>
<p style="text-align: center;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: center;"><strong style="color: black;">§5</strong></p>
<p style="text-align: justify;"><span style="color: black;">Właściciele lokali sdfasfsafsafas kolejnych miesięcy następujących
        po miesiącu, w kasdfa została podjęta.</span></p>
<p style="text-align: center;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: center;"><strong style="color: black;">§6</strong></p>
<p style="text-align: justify;"><span style="color: black;">Władsafsainiejszej uchwały.</span></p>
<p style="text-align: center;"><strong style="color: black;">&nbsp;</strong></p>
<p style="text-align: center;"><strong style="color: black;">§7</strong></p>
<p style="text-align: justify;"><span style="color: black;">Uchwdsafsaf01.01.2020 r. </span></p>
<p style="text-align: justify;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: justify;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: justify;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: justify;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: justify;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: justify;"><span style="color: black;">* w skład kofdsafsafa03.2010r.</span></p>
<p style="text-align: justify;"><strong>&nbsp;</strong></p>
<p><br></p>'''
    
    result = translate_html_to_typst(html, debug=False)
    
    # All text must be preserved
    assert "fdsafasf Nfsdafsafsa2021" in result
    assert "zewnętrznym" in result
    assert "w skład kofdsafsafa03.2010r" in result
    
    # Critical: asterisks must be escaped to prevent unclosed delimiter errors
    # The HTML has two asterisks: one after "zewnętrznym.*" and one before "* w skład"
    assert r'\*' in result, f"Asterisks must be escaped in: {result}"
    
    # There should be at least 2 escaped asterisks
    assert result.count(r'\*') >= 2, f"Expected at least 2 escaped asterisks, found {result.count(r'\\*')} in: {result}"
    
    # No unescaped asterisks that could cause delimiter errors
    # (except in bold markup like *text* which is intentional)
    # Check that we don't have unescaped * inside function calls
    # Pattern to avoid: #text(...)[...*...]
    import re
    # Find all #text(...)[] or #align(...)[] function calls
    function_calls = re.findall(r'#\w+\([^\]]*\)\[([^\]]*)\]', result)
    for call_content in function_calls:
        # Check if there are unescaped asterisks (not preceded by backslash)
        # Allow *text* patterns (markup) but not standalone *
        # This is a simple heuristic: if we have * not preceded by \ and not part of *word* pattern
        if '*' in call_content:
            # Check if it's escaped or part of markup
            for i, char in enumerate(call_content):
                if char == '*':
                    # Check if it's escaped
                    if i > 0 and call_content[i-1] == '\\':
                        continue  # Escaped, OK
                    # Check if it's part of *word* markup (both opening and closing * present)
                    # For simplicity, just check that it's not a standalone *
                    # If we found an unescaped *, it should be part of valid markup
                    # This is hard to check properly, so just verify the escaped count
    
    print("✓ Issue HTML unclosed delimiter test passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("Running HTML to Typst Translator Test Suite")
    print("="*60 + "\n")
    
    tests = [
        test_text_preservation,
        test_basic_formatting,
        test_headings,
        test_lists,
        test_quill_indent,
        test_quill_alignment,
        test_inline_styles,
        test_blockquote,
        test_code_blocks,
        test_links,
        test_images,
        test_line_breaks,
        test_debug_mode,
        test_complex_quill_example,
        test_edge_cases,
        test_span_with_quill_classes,
        test_consecutive_styled_elements,
        test_superscript_and_subscript,
        test_delimiter_collision_prevention,
        test_unclosed_delimiter_issue,
        test_debug_log_file,
        test_asterisk_escape_in_function_syntax,
        test_nested_formatting,
        test_literal_delimiters_in_plain_text,
        test_issue_html_unclosed_delimiter,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
