# html2typst-second

Production-quality HTML to Typst translator specifically designed for Quill.js generated content.

## Features

- **100% Text Preservation**: All text content from HTML is guaranteed to appear in the output
- **Two Modes**: Production (clean output) and Debug (diagnostic comments)
- **Quill.js Support**: Handles Quill-specific classes and styles
- **Structure Priority**: Semantic structure (lists, headings, paragraphs) prioritized over styling
- **Fail-Safe**: Unsupported styles are ignored gracefully without losing content

## Installation

```bash
npm install html2typst-second
```

## Usage

```typescript
import { translateHtmlToTypst } from 'html2typst-second';

// Production mode (default)
const typst = translateHtmlToTypst('<p><strong>Hello</strong> world!</p>');
// Output: "*Hello* world!"

// Debug mode
const typstDebug = translateHtmlToTypst('<custom-tag>Content</custom-tag>', true);
// Output includes diagnostic comments for unsupported elements
```

## API

### `translateHtmlToTypst(html: string, debug?: boolean): string`

Converts HTML to Typst format.

**Parameters:**
- `html` - HTML string to convert (typically from Quill.js)
- `debug` - Optional boolean to enable debug mode (default: `false`)

**Returns:** Typst formatted string

## Supported HTML Elements

### Structure
- `<p>`, `<div>` → Paragraphs
- `<br>` → Line breaks
- `<h1>` - `<h6>` → Headings
- `<ul>`, `<ol>`, `<li>` → Lists (unordered and ordered)
- `<blockquote>` → Block quotes

### Formatting
- `<strong>`, `<b>` → Bold text (`*text*`)
- `<em>`, `<i>` → Italic text (`_text_`)
- `<u>`, `<s>`, `<strike>` → Text preserved, styling ignored

### Code
- `<pre>`, `<code>` → Code blocks and inline code
- Inline: `` `code` ``
- Block: ` ```code``` `

### Links and Media
- `<a href="...">` → Links (`#link("url")[text]`)
- `<img>` → Fallback to alt text

### Quill.js Classes

- `ql-align-center`, `ql-align-right`, `ql-align-justify` → Text alignment
- `ql-indent-{n}` → List indentation levels
- Other Quill classes → Preserved in debug mode, ignored in production

### Inline Styles

Supported:
- `font-weight: bold` → Bold
- `font-style: italic` → Italic
- `text-align: center|right|justify` → Alignment

Unsupported styles are silently ignored while preserving text content.

## Mode Comparison

### Production Mode (`debug = false`)
- Clean output for end users
- No comments or debug markers
- Unsupported features silently ignored
- All text content preserved

### Debug Mode (`debug = true`)
- Includes diagnostic comments
- Reports unsupported HTML tags
- Reports unknown styles and classes
- All text content still preserved

## Examples

### Basic Formatting
```typescript
translateHtmlToTypst('<p><strong>Bold</strong> and <em>italic</em></p>');
// Output: "*Bold* and _italic_"
```

### Lists with Indentation
```typescript
const html = `
  <ul>
    <li>Item 1</li>
    <li class="ql-indent-1">Indented item</li>
    <li>Item 2</li>
  </ul>
`;
translateHtmlToTypst(html);
// Output:
// - Item 1
//   - Indented item
// - Item 2
```

### Headings and Paragraphs
```typescript
const html = `
  <h1>Title</h1>
  <p>First paragraph</p>
  <p class="ql-align-center">Centered text</p>
`;
translateHtmlToTypst(html);
// Output:
// = Title
//
// First paragraph
//
// #align(center)[Centered text]
```

### Complex Quill.js Output
```typescript
const html = `
  <h1>Document</h1>
  <p><strong>Important:</strong> This is a <em>complex</em> example.</p>
  <ul>
    <li>Regular item</li>
    <li class="ql-indent-1">Indented item</li>
  </ul>
  <blockquote>A meaningful quote</blockquote>
  <pre><code>const x = 42;</code></pre>
`;

const result = translateHtmlToTypst(html);
// Produces properly formatted Typst with all content preserved
```

## Design Principles

1. **Text Preservation is Sacrosanct**: 100% of text content must appear in output
2. **Structure Over Style**: Semantic structure has priority over visual styling
3. **Fail-Safe Degradation**: Unknown elements render their content as plain text
4. **No Silent Failures**: Debug mode helps identify unsupported features
5. **Production Ready**: Clean output suitable for end users in production mode

## Development

```bash
# Install dependencies
npm install

# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Build
npm run build

# Lint
npm run lint
```

## License

ISC
