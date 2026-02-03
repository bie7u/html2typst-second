"""
Example usage of the HTML to Typst translator.

This script demonstrates how to use the translator with various HTML examples,
including real-world Quill.js generated content.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from html2typst import translate_html_to_typst


def print_example(title: str, html: str, debug: bool = False):
    """Print an example conversion."""
    print("\n" + "="*70)
    print(f"Example: {title}")
    print("="*70)
    print("\nInput HTML:")
    print(html)
    print("\nOutput Typst:")
    result = translate_html_to_typst(html, debug=debug)
    print(result)
    print("-"*70)


def main():
    """Run example conversions."""
    print("HTML to Typst Translator - Examples")
    print("="*70)
    
    # Example 1: Basic formatting
    print_example(
        "Basic Formatting",
        "<p>This is <strong>bold</strong> and <em>italic</em> text.</p>"
    )
    
    # Example 2: Headings
    print_example(
        "Headings",
        """
        <h1>Main Title</h1>
        <h2>Subtitle</h2>
        <p>Content paragraph.</p>
        """
    )
    
    # Example 3: Lists
    print_example(
        "Lists",
        """
        <ul>
            <li>First item</li>
            <li>Second item</li>
            <li>Third item</li>
        </ul>
        <ol>
            <li>Numbered one</li>
            <li>Numbered two</li>
        </ol>
        """
    )
    
    # Example 4: Quill.js indentation
    print_example(
        "Quill.js Indented Lists",
        """
        <ul>
            <li>Level 0</li>
            <li class="ql-indent-1">Level 1 indented</li>
            <li class="ql-indent-2">Level 2 indented</li>
            <li>Back to level 0</li>
        </ul>
        """
    )
    
    # Example 5: Quill.js alignment
    print_example(
        "Quill.js Text Alignment",
        """
        <p>Default left alignment</p>
        <p class="ql-align-center">Centered text</p>
        <p class="ql-align-right">Right-aligned text</p>
        """
    )
    
    # Example 6: Styled spans
    print_example(
        "Styled Spans",
        """
        <p>
            <span style="color: red;">Red text</span>,
            <span style="color: blue;">blue text</span>, and
            <span style="font-size: 20px;">larger text</span>.
        </p>
        """
    )
    
    # Example 7: Code blocks
    print_example(
        "Code Blocks",
        """
        <p>Use the <code>print()</code> function in Python.</p>
        <pre><code>def hello():
    print("Hello, world!")
    return True</code></pre>
        """
    )
    
    # Example 8: Blockquotes
    print_example(
        "Blockquotes",
        """
        <p>As someone once said:</p>
        <blockquote>This is a famous quote that should be highlighted.</blockquote>
        <p>And that's true!</p>
        """
    )
    
    # Example 9: Links and images
    print_example(
        "Links and Images",
        """
        <p>Visit <a href="https://typst.app">Typst</a> for more info.</p>
        <img src="logo.png" alt="Company Logo" />
        """
    )
    
    # Example 10: Complex Quill.js document
    print_example(
        "Complex Quill.js Document",
        """
        <h1>Project Documentation</h1>
        <p class="ql-align-center"><em>Version 1.0</em></p>
        
        <h2>Introduction</h2>
        <p>This document contains <strong>important</strong> information about the project.</p>
        
        <h2>Features</h2>
        <ul>
            <li>Feature one with <code>code</code></li>
            <li class="ql-indent-1">Sub-feature A</li>
            <li class="ql-indent-1">Sub-feature B</li>
            <li>Feature two</li>
        </ul>
        
        <h2>Notes</h2>
        <blockquote>Remember to test thoroughly!</blockquote>
        
        <p>For more info, visit <a href="https://example.com">our website</a>.</p>
        """
    )
    
    # Example 11: Debug mode
    print("\n" + "="*70)
    print("Example: Debug Mode (with unsupported elements)")
    print("="*70)
    html_debug = """
    <p>Normal text with <custom>custom tag</custom> and
    <span style="text-shadow: 2px 2px;">unsupported style</span>.</p>
    """
    print("\nInput HTML:")
    print(html_debug)
    print("\nOutput Typst (debug=True):")
    result = translate_html_to_typst(html_debug, debug=True)
    print(result)
    print("-"*70)
    
    print("\n\n✓ All examples completed successfully!")


if __name__ == "__main__":
    main()
