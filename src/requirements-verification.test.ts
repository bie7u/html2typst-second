/**
 * Verification tests to ensure all requirements from the problem statement are met
 */

import { translateHtmlToTypst } from './translator';

describe('Problem Statement Requirements Verification', () => {
  describe('API Requirements', () => {
    test('should export translateHtmlToTypst function with correct signature', () => {
      expect(typeof translateHtmlToTypst).toBe('function');
      // Function has 1 required parameter (html) and 1 optional (debug)
      expect(translateHtmlToTypst.length).toBe(1);
    });

    test('should accept html string and optional debug boolean', () => {
      expect(() => translateHtmlToTypst('<p>test</p>')).not.toThrow();
      expect(() => translateHtmlToTypst('<p>test</p>', false)).not.toThrow();
      expect(() => translateHtmlToTypst('<p>test</p>', true)).not.toThrow();
    });

    test('should return string', () => {
      const result = translateHtmlToTypst('<p>test</p>');
      expect(typeof result).toBe('string');
    });
  });

  describe('Production Mode (debug = false)', () => {
    test('should produce clean output without debug comments', () => {
      const result = translateHtmlToTypst('<unknown-tag>content</unknown-tag>', false);
      expect(result).not.toContain('/*');
      expect(result).not.toContain('Unsupported');
      expect(result).toContain('content');
    });

    test('should silently ignore unsupported styles', () => {
      const html = '<p style="background-color: red; border: 1px solid;">text</p>';
      const result = translateHtmlToTypst(html, false);
      expect(result).toContain('text');
      expect(result).not.toContain('background-color');
      expect(result).not.toContain('border');
    });

    test('should silently ignore unsupported Quill classes', () => {
      const html = '<span class="ql-custom-unknown">text</span>';
      const result = translateHtmlToTypst(html, false);
      expect(result).toContain('text');
      expect(result).not.toContain('ql-custom-unknown');
    });
  });

  describe('Debug Mode (debug = true)', () => {
    test('should include diagnostic comments for unsupported tags', () => {
      const result = translateHtmlToTypst('<custom-tag>content</custom-tag>', true);
      expect(result).toContain('Unsupported tag');
      expect(result).toContain('content');
    });

    test('should preserve all text even in debug mode', () => {
      const result = translateHtmlToTypst('<unknown>text1</unknown><p>text2</p>', true);
      expect(result).toContain('text1');
      expect(result).toContain('text2');
    });
  });

  describe('100% Text Preservation (CRITICAL)', () => {
    test('should preserve all text in complex nested structure', () => {
      const html = `
        <div>
          <h1>Title</h1>
          <p>Paragraph <strong>bold</strong> <em>italic</em></p>
          <ul>
            <li>Item 1</li>
            <li class="ql-indent-1">Item 2</li>
          </ul>
          <unknown-tag>Unknown content</unknown-tag>
          <span style="color: red;">Styled span</span>
        </div>
      `;
      const result = translateHtmlToTypst(html);
      
      expect(result).toContain('Title');
      expect(result).toContain('Paragraph');
      expect(result).toContain('bold');
      expect(result).toContain('italic');
      expect(result).toContain('Item 1');
      expect(result).toContain('Item 2');
      expect(result).toContain('Unknown content');
      expect(result).toContain('Styled span');
    });

    test('should never lose text due to unsupported features', () => {
      const html = `
        <p style="unknown-style: value;">Text 1</p>
        <div class="unknown-class">Text 2</div>
        <custom-element>Text 3</custom-element>
        <span style="color: purple; font-family: unknown;">Text 4</span>
      `;
      const result = translateHtmlToTypst(html);
      
      expect(result).toContain('Text 1');
      expect(result).toContain('Text 2');
      expect(result).toContain('Text 3');
      expect(result).toContain('Text 4');
    });

    test('should preserve text in deeply nested unknown tags', () => {
      const html = '<unknown1><unknown2><unknown3>Deep text</unknown3></unknown2></unknown1>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Deep text');
    });
  });

  describe('Structure > Style Priority', () => {
    test('should preserve list structure even with unsupported styles', () => {
      const html = `
        <ul>
          <li style="color: red; background: yellow;">Item with styles</li>
        </ul>
      `;
      const result = translateHtmlToTypst(html);
      expect(result).toContain('- Item with styles');
    });

    test('should preserve heading structure regardless of styles', () => {
      const html = '<h1 style="font-size: 48px; color: blue;">Heading</h1>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('= Heading');
    });

    test('should preserve paragraph structure with unsupported classes', () => {
      const html = '<p class="unknown-class-1 unknown-class-2">Text</p>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Text');
    });
  });

  describe('Quill.js Specific Features', () => {
    test('should handle ql-indent classes correctly', () => {
      const html = `
        <li class="ql-indent-1" style="text-align: justify;">
          <span style="color: windowtext;">text</span>
        </li>
      `;
      const result = translateHtmlToTypst(html);
      expect(result).toContain('text');
      // Should have indentation
      expect(result.indexOf('text')).toBeGreaterThan(2);
    });

    test('should handle ql-align classes', () => {
      const html = '<p class="ql-align-center">centered</p>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('centered');
      expect(result).toContain('#align(center)');
    });

    test('should preserve text in span with unsupported Quill styles', () => {
      const html = '<span class="ql-size-large ql-font-serif">Text</span>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Text');
    });
  });

  describe('Basic HTML Mappings', () => {
    test('should map <p> and <div> to paragraphs', () => {
      expect(translateHtmlToTypst('<p>P text</p>')).toContain('P text');
      expect(translateHtmlToTypst('<div>Div text</div>')).toContain('Div text');
    });

    test('should map <br> to newline', () => {
      const result = translateHtmlToTypst('<p>Line1<br>Line2</p>');
      expect(result).toMatch(/Line1\s*\n\s*Line2/);
    });

    test('should map <strong> and <b> to bold', () => {
      expect(translateHtmlToTypst('<strong>Bold</strong>')).toContain('*Bold*');
      expect(translateHtmlToTypst('<b>Bold</b>')).toContain('*Bold*');
    });

    test('should map <em> and <i> to italic', () => {
      expect(translateHtmlToTypst('<em>Italic</em>')).toContain('_Italic_');
      expect(translateHtmlToTypst('<i>Italic</i>')).toContain('_Italic_');
    });

    test('should preserve text in <u> and <s> without styling', () => {
      expect(translateHtmlToTypst('<u>Underline</u>')).toContain('Underline');
      expect(translateHtmlToTypst('<s>Strike</s>')).toContain('Strike');
    });

    test('should map headings correctly', () => {
      expect(translateHtmlToTypst('<h1>H1</h1>')).toContain('= H1');
      expect(translateHtmlToTypst('<h2>H2</h2>')).toContain('== H2');
      expect(translateHtmlToTypst('<h3>H3</h3>')).toContain('=== H3');
    });

    test('should map lists correctly', () => {
      const ul = translateHtmlToTypst('<ul><li>Item</li></ul>');
      expect(ul).toContain('- Item');
      
      const ol = translateHtmlToTypst('<ol><li>Item</li></ol>');
      expect(ol).toContain('+ Item');
    });

    test('should map blockquote correctly', () => {
      const result = translateHtmlToTypst('<blockquote>Quote</blockquote>');
      expect(result).toContain('> Quote');
    });

    test('should map code blocks correctly', () => {
      const result = translateHtmlToTypst('<pre><code>code</code></pre>');
      expect(result).toContain('```');
      expect(result).toContain('code');
    });

    test('should map inline code correctly', () => {
      const result = translateHtmlToTypst('<p><code>code</code></p>');
      expect(result).toContain('`code`');
    });

    test('should map links correctly', () => {
      const result = translateHtmlToTypst('<a href="url">text</a>');
      expect(result).toContain('#link("url")[text]');
    });

    test('should fallback to text for links without href', () => {
      const result = translateHtmlToTypst('<a>text</a>');
      expect(result).toContain('text');
      expect(result).not.toContain('#link');
    });

    test('should fallback to alt text for images', () => {
      const result = translateHtmlToTypst('<img src="img.png" alt="description">');
      expect(result).toContain('description');
    });
  });

  describe('Inline Styles Support', () => {
    test('should handle font-weight: bold', () => {
      const result = translateHtmlToTypst('<span style="font-weight: bold;">Bold</span>');
      expect(result).toContain('*Bold*');
    });

    test('should handle font-style: italic', () => {
      const result = translateHtmlToTypst('<span style="font-style: italic;">Italic</span>');
      expect(result).toContain('_Italic_');
    });

    test('should handle text-align styles', () => {
      const result = translateHtmlToTypst('<p style="text-align: center;">Text</p>');
      expect(result).toContain('#align(center)');
    });

    test('should preserve text even with unsupported inline styles', () => {
      const html = '<span style="color: red; background: blue; border: 1px;">Text</span>';
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Text');
    });
  });

  describe('Fail-Safe Behavior', () => {
    test('should not fail on empty HTML', () => {
      expect(() => translateHtmlToTypst('')).not.toThrow();
      expect(translateHtmlToTypst('')).toBe('');
    });

    test('should not fail on malformed HTML', () => {
      expect(() => translateHtmlToTypst('<p>Unclosed paragraph')).not.toThrow();
    });

    test('should not fail on deeply nested structures', () => {
      let html = 'text';
      for (let i = 0; i < 50; i++) {
        html = `<div>${html}</div>`;
      }
      expect(() => translateHtmlToTypst(html)).not.toThrow();
      expect(translateHtmlToTypst(html)).toContain('text');
    });

    test('should handle mixed content gracefully', () => {
      const html = 'Text before <p>Para</p> text after <unknown>more</unknown> end';
      expect(() => translateHtmlToTypst(html)).not.toThrow();
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Text before');
      expect(result).toContain('Para');
      expect(result).toContain('text after');
      expect(result).toContain('more');
      expect(result).toContain('end');
    });
  });

  describe('Real-World Quill.js Examples', () => {
    test('should handle typical Quill.js rich text', () => {
      const html = `
        <h1>Document Title</h1>
        <p><strong>Introduction:</strong> This is a <em>sample</em> document.</p>
        <ul>
          <li>First point</li>
          <li class="ql-indent-1">Sub-point</li>
          <li>Second point</li>
        </ul>
        <p class="ql-align-center">Centered conclusion</p>
      `;
      
      const result = translateHtmlToTypst(html);
      
      // All text preserved
      expect(result).toContain('Document Title');
      expect(result).toContain('Introduction:');
      expect(result).toContain('sample');
      expect(result).toContain('First point');
      expect(result).toContain('Sub-point');
      expect(result).toContain('Second point');
      expect(result).toContain('Centered conclusion');
      
      // Structure preserved
      expect(result).toContain('= Document Title');
      expect(result).toContain('*Introduction:*');
      expect(result).toContain('_sample_');
      expect(result).toContain('- First point');
      expect(result).toContain('#align(center)');
    });

    test('should handle Quill.js code blocks', () => {
      const html = `
        <p>Here's some code:</p>
        <pre data-language="javascript"><code>function hello() {
  console.log("Hello, world!");
}</code></pre>
        <p>End of code</p>
      `;
      
      const result = translateHtmlToTypst(html);
      expect(result).toContain("Here's some code");
      expect(result).toContain('```');
      expect(result).toContain('function hello()');
      expect(result).toContain('console.log');
      expect(result).toContain('End of code');
    });

    test('should handle Quill.js with mixed inline styles', () => {
      const html = `
        <p>
          <span style="font-weight: bold;">Bold text</span>
          <span style="font-style: italic;">Italic text</span>
          <span style="color: red;">Colored text</span>
        </p>
      `;
      
      const result = translateHtmlToTypst(html);
      expect(result).toContain('Bold text');
      expect(result).toContain('Italic text');
      expect(result).toContain('Colored text');
      expect(result).toContain('*Bold text*');
      expect(result).toContain('_Italic text_');
    });
  });
});
