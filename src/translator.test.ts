import { translateHtmlToTypst } from './translator';

describe('translateHtmlToTypst', () => {
  describe('Basic text and paragraphs', () => {
    test('should handle empty input', () => {
      expect(translateHtmlToTypst('')).toBe('');
      expect(translateHtmlToTypst('   ')).toBe('');
    });

    test('should handle plain text', () => {
      const result = translateHtmlToTypst('Hello world');
      expect(result).toContain('Hello world');
    });

    test('should handle paragraph', () => {
      const result = translateHtmlToTypst('<p>Hello world</p>');
      expect(result).toContain('Hello world');
      expect(result.trim()).toMatch(/Hello world\s*$/);
    });

    test('should handle multiple paragraphs', () => {
      const result = translateHtmlToTypst('<p>First paragraph</p><p>Second paragraph</p>');
      expect(result).toContain('First paragraph');
      expect(result).toContain('Second paragraph');
    });

    test('should handle div as paragraph', () => {
      const result = translateHtmlToTypst('<div>Content in div</div>');
      expect(result).toContain('Content in div');
    });

    test('should handle line breaks', () => {
      const result = translateHtmlToTypst('<p>Line one<br>Line two</p>');
      expect(result).toContain('Line one');
      expect(result).toContain('Line two');
      expect(result).toMatch(/Line one\nLine two/);
    });
  });

  describe('Text formatting', () => {
    test('should handle bold with strong', () => {
      const result = translateHtmlToTypst('<p><strong>Bold text</strong></p>');
      expect(result).toContain('*Bold text*');
    });

    test('should handle bold with b', () => {
      const result = translateHtmlToTypst('<p><b>Bold text</b></p>');
      expect(result).toContain('*Bold text*');
    });

    test('should handle italic with em', () => {
      const result = translateHtmlToTypst('<p><em>Italic text</em></p>');
      expect(result).toContain('_Italic text_');
    });

    test('should handle italic with i', () => {
      const result = translateHtmlToTypst('<p><i>Italic text</i></p>');
      expect(result).toContain('_Italic text_');
    });

    test('should handle bold and italic combined', () => {
      const result = translateHtmlToTypst('<p><strong><em>Bold italic</em></strong></p>');
      // Both * and _ should be present
      expect(result).toContain('Bold italic');
      expect(result).toContain('*');
      expect(result).toContain('_');
    });

    test('should preserve text when underline is used', () => {
      const result = translateHtmlToTypst('<p><u>Underlined text</u></p>');
      expect(result).toContain('Underlined text');
    });

    test('should preserve text when strikethrough is used', () => {
      const result = translateHtmlToTypst('<p><s>Strikethrough text</s></p>');
      expect(result).toContain('Strikethrough text');
    });
  });

  describe('Headings', () => {
    test('should handle h1', () => {
      const result = translateHtmlToTypst('<h1>Heading 1</h1>');
      expect(result).toContain('= Heading 1');
    });

    test('should handle h2', () => {
      const result = translateHtmlToTypst('<h2>Heading 2</h2>');
      expect(result).toContain('== Heading 2');
    });

    test('should handle h3', () => {
      const result = translateHtmlToTypst('<h3>Heading 3</h3>');
      expect(result).toContain('=== Heading 3');
    });

    test('should handle h4', () => {
      const result = translateHtmlToTypst('<h4>Heading 4</h4>');
      expect(result).toContain('==== Heading 4');
    });

    test('should handle h5', () => {
      const result = translateHtmlToTypst('<h5>Heading 5</h5>');
      expect(result).toContain('===== Heading 5');
    });

    test('should handle h6', () => {
      const result = translateHtmlToTypst('<h6>Heading 6</h6>');
      expect(result).toContain('====== Heading 6');
    });
  });

  describe('Lists', () => {
    test('should handle unordered list', () => {
      const html = '<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('- Item 1');
      expect(result).toContain('- Item 2');
      expect(result).toContain('- Item 3');
    });

    test('should handle ordered list', () => {
      const html = '<ol><li>First</li><li>Second</li><li>Third</li></ol>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('+ First');
      expect(result).toContain('+ Second');
      expect(result).toContain('+ Third');
    });

    test('should handle nested lists', () => {
      const html = '<ul><li>Item 1<ul><li>Nested 1</li><li>Nested 2</li></ul></li><li>Item 2</li></ul>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('- Item 1');
      expect(result).toContain('  - Nested 1');
      expect(result).toContain('  - Nested 2');
      expect(result).toContain('- Item 2');
    });
  });

  describe('Quill.js indent classes', () => {
    test('should handle ql-indent-1', () => {
      const html = '<ul><li class="ql-indent-1">Indented item</li></ul>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('  - Indented item');
    });

    test('should handle ql-indent-2', () => {
      const html = '<ul><li class="ql-indent-2">Double indented</li></ul>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('    - Double indented');
    });

    test('should preserve text even with unsupported indent levels', () => {
      const html = '<ul><li class="ql-indent-5">Deep indent</li></ul>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Deep indent');
    });
  });

  describe('Quill.js alignment classes', () => {
    test('should handle ql-align-center', () => {
      const html = '<p class="ql-align-center">Centered text</p>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('#align(center)[Centered text]');
    });

    test('should handle ql-align-right', () => {
      const html = '<p class="ql-align-right">Right aligned</p>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('#align(right)[Right aligned]');
    });

    test('should handle ql-align-justify', () => {
      const html = '<p class="ql-align-justify">Justified text</p>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Justified text');
      // Justify maps to center in Typst
      expect(result).toContain('#align(center)');
    });

    test('should handle inline text-align style', () => {
      const html = '<p style="text-align: center;">Centered via style</p>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('#align(center)[Centered via style]');
    });
  });

  describe('Blockquotes', () => {
    test('should handle blockquote', () => {
      const html = '<blockquote>This is a quote</blockquote>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('> This is a quote');
    });

    test('should handle multiline blockquote', () => {
      const html = '<blockquote>Line 1<br>Line 2</blockquote>';
      const result = translateHtmlToTypst(html);
      expect(result).toMatch(/> Line 1[\s\S]*> Line 2/);
    });
  });

  describe('Code blocks', () => {
    test('should handle pre element', () => {
      const html = '<pre>const x = 42;</pre>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('```');
      expect(result).toContain('const x = 42;');
    });

    test('should handle pre with code element', () => {
      const html = '<pre><code>function test() { return true; }</code></pre>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('```');
      expect(result).toContain('function test() { return true; }');
    });

    test('should handle inline code', () => {
      const html = '<p>Use <code>console.log()</code> for debugging</p>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('`console.log()`');
    });
  });

  describe('Links', () => {
    test('should handle link with href', () => {
      const html = '<a href="https://example.com">Example</a>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('#link("https://example.com")[Example]');
    });

    test('should handle link without href', () => {
      const html = '<a>Just text</a>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Just text');
      expect(result).not.toContain('#link');
    });

    test('should preserve text in links', () => {
      const html = '<a href="#">Important link text</a>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Important link text');
    });
  });

  describe('Images', () => {
    test('should fallback to alt text for images', () => {
      const html = '<img src="image.png" alt="Description">';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Description');
    });

    test('should handle image without alt text', () => {
      const html = '<img src="image.png">';
      const result = translateHtmlToTypst(html);
      // Should not fail, may be empty or minimal output
      expect(result).toBeDefined();
    });

    test('should include debug info for images in debug mode', () => {
      const html = '<img src="image.png" alt="Desc">';
      const result = translateHtmlToTypst(html, true);
      expect(result).toContain('image.png');
    });
  });

  describe('Span elements', () => {
    test('should preserve text in span', () => {
      const html = '<p><span>Text in span</span></p>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Text in span');
    });

    test('should handle span with bold style', () => {
      const html = '<p><span style="font-weight: bold;">Bold span</span></p>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('*Bold span*');
    });

    test('should handle span with italic style', () => {
      const html = '<p><span style="font-style: italic;">Italic span</span></p>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('_Italic span_');
    });

    test('should preserve text even with unsupported span styles', () => {
      const html = '<p><span style="color: red;">Red text</span></p>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Red text');
    });
  });

  describe('Text preservation', () => {
    test('should preserve all text content', () => {
      const html = `
        <h1>Title</h1>
        <p>First paragraph with <strong>bold</strong> and <em>italic</em>.</p>
        <ul>
          <li>List item 1</li>
          <li>List item 2</li>
        </ul>
        <p>Last paragraph</p>
      `;
      const result = translateHtmlToTypst(html);
      
      expect(result).toContain('Title');
      expect(result).toContain('First paragraph');
      expect(result).toContain('bold');
      expect(result).toContain('italic');
      expect(result).toContain('List item 1');
      expect(result).toContain('List item 2');
      expect(result).toContain('Last paragraph');
    });

    test('should preserve text in unknown tags', () => {
      const html = '<custom-tag>Text in custom tag</custom-tag>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Text in custom tag');
    });

    test('should preserve text with multiple unsupported styles', () => {
      const html = '<p style="background: yellow; border: 1px solid;">Important text</p>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Important text');
    });
  });

  describe('Debug mode', () => {
    test('should not include debug comments in production mode', () => {
      const html = '<custom-tag>Content</custom-tag>';
      const result = translateHtmlToTypst(html, false);
      expect(result).not.toContain('/*');
      expect(result).not.toContain('Unsupported');
      expect(result).toContain('Content');
    });

    test('should include debug comments for unsupported tags in debug mode', () => {
      const html = '<custom-tag>Content</custom-tag>';
      const result = translateHtmlToTypst(html, true);
      expect(result).toContain('Unsupported tag');
      expect(result).toContain('Content');
    });

    test('should not report common tags as unsupported', () => {
      const html = '<html><body><p>Text</p></body></html>';
      const result = translateHtmlToTypst(html, true);
      expect(result).not.toContain('Unsupported tag: html');
      expect(result).not.toContain('Unsupported tag: body');
      expect(result).toContain('Text');
    });
  });

  describe('Complex Quill.js examples', () => {
    test('should handle list item with indent and alignment', () => {
      const html = `<li class="ql-indent-1" style="text-align: justify;">
        <span style="color: windowtext;">List item text</span>
      </li>`;
      const result = translateHtmlToTypst(html);
      expect(result).toContain('List item text');
      // Should handle indent
      expect(result).toMatch(/\s+-\s+List item text/);
    });

    test('should handle complex nested structure', () => {
      const html = `
        <div class="ql-align-center">
          <span style="font-weight: bold;">
            <span style="font-style: italic;">Bold and italic</span>
          </span>
        </div>
      `;
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Bold and italic');
      expect(result).toContain('*');
      expect(result).toContain('_');
    });

    test('should handle real Quill.js output', () => {
      const html = `
        <h1>Document Title</h1>
        <p><strong>Bold paragraph</strong> with normal text.</p>
        <ul>
          <li>First item</li>
          <li class="ql-indent-1">Indented item</li>
          <li>Back to normal</li>
        </ul>
        <p class="ql-align-center">Centered paragraph</p>
        <blockquote>This is a quote from someone</blockquote>
        <pre><code>const code = "example";</code></pre>
      `;
      const result = translateHtmlToTypst(html);
      
      // Verify all text is present
      expect(result).toContain('Document Title');
      expect(result).toContain('Bold paragraph');
      expect(result).toContain('normal text');
      expect(result).toContain('First item');
      expect(result).toContain('Indented item');
      expect(result).toContain('Back to normal');
      expect(result).toContain('Centered paragraph');
      expect(result).toContain('This is a quote from someone');
      expect(result).toContain('const code = "example";');
      
      // Verify structure
      expect(result).toContain('= Document Title');
      expect(result).toContain('*Bold paragraph*');
      expect(result).toContain('- First item');
      expect(result).toContain('  - Indented item');
      expect(result).toContain('#align(center)');
      expect(result).toContain('>');
      expect(result).toContain('```');
    });
  });

  describe('Edge cases', () => {
    test('should handle empty elements', () => {
      const html = '<p></p><div></div><span></span>';
      const result = translateHtmlToTypst(html);
      // Should not fail
      expect(result).toBeDefined();
    });

    test('should handle deeply nested elements', () => {
      const html = '<div><div><div><div><p>Deep text</p></div></div></div></div>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Deep text');
    });

    test('should handle mixed content', () => {
      const html = '<p>Text before <strong>bold</strong> text after</p>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Text before');
      expect(result).toContain('*bold*');
      expect(result).toContain('text after');
    });

    test('should handle special characters', () => {
      const html = '<p>Special chars: &lt; &gt; &amp; &quot;</p>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('<');
      expect(result).toContain('>');
      expect(result).toContain('&');
    });
  });
});
