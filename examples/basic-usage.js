const { translateHtmlToTypst } = require('../dist/index');

// Example 1: Basic formatting
console.log('=== Example 1: Basic Formatting ===');
const html1 = '<p><strong>Bold text</strong> and <em>italic text</em></p>';
console.log('HTML:', html1);
console.log('Typst:', translateHtmlToTypst(html1));
console.log();

// Example 2: Headings
console.log('=== Example 2: Headings ===');
const html2 = '<h1>Main Title</h1><h2>Subtitle</h2><p>Content here</p>';
console.log('HTML:', html2);
console.log('Typst:');
console.log(translateHtmlToTypst(html2));
console.log();

// Example 3: Lists with indentation
console.log('=== Example 3: Lists with Quill.js Indentation ===');
const html3 = `
<ul>
  <li>Regular item</li>
  <li class="ql-indent-1">Indented level 1</li>
  <li class="ql-indent-2">Indented level 2</li>
  <li>Back to regular</li>
</ul>
`;
console.log('HTML:', html3);
console.log('Typst:');
console.log(translateHtmlToTypst(html3));
console.log();

// Example 4: Text alignment
console.log('=== Example 4: Text Alignment ===');
const html4 = `
<p>Normal paragraph</p>
<p class="ql-align-center">Centered paragraph</p>
<p class="ql-align-right">Right aligned</p>
`;
console.log('HTML:', html4);
console.log('Typst:');
console.log(translateHtmlToTypst(html4));
console.log();

// Example 5: Complex Quill.js document
console.log('=== Example 5: Complex Quill.js Document ===');
const html5 = `
<h1>Meeting Notes</h1>
<p><strong>Date:</strong> 2024-02-03</p>
<p><em>Attendees:</em> Alice, Bob, Charlie</p>

<h2>Agenda</h2>
<ol>
  <li>Review last meeting</li>
  <li>Discuss new features
    <ul>
      <li class="ql-indent-1">Feature A</li>
      <li class="ql-indent-1">Feature B</li>
    </ul>
  </li>
  <li>Next steps</li>
</ol>

<h2>Action Items</h2>
<blockquote>Remember to follow up on the client feedback</blockquote>

<p>Code snippet for reference:</p>
<pre><code>function processData(input) {
  return input.map(x => x * 2);
}</code></pre>

<p class="ql-align-center"><strong>End of Notes</strong></p>
`;
console.log('Typst Output:');
console.log(translateHtmlToTypst(html5));
console.log();

// Example 6: Debug mode
console.log('=== Example 6: Debug Mode ===');
const html6 = '<custom-element>This is unsupported</custom-element><p>Normal text</p>';
console.log('HTML:', html6);
console.log('Production mode:');
console.log(translateHtmlToTypst(html6, false));
console.log('\nDebug mode:');
console.log(translateHtmlToTypst(html6, true));
