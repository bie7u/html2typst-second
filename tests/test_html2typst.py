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
    
    # Unsupported tag
    html = "<p>Text with <custom>custom tag</custom></p>"
    result_prod = translate_html_to_typst(html, debug=False)
    result_debug = translate_html_to_typst(html, debug=True)
    
    # Both should preserve text
    assert "custom tag" in result_prod
    assert "custom tag" in result_debug
    
    # Debug should have comments
    assert "/*" not in result_prod  # No debug comments in production
    
    # Unsupported style
    html = '<span style="text-shadow: 2px 2px;">Shadowed</span>'
    result_debug = translate_html_to_typst(html, debug=True)
    assert "Shadowed" in result_debug  # Text preserved
    
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
