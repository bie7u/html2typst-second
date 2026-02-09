#!/usr/bin/env python3
"""Test script to reproduce the unclosed delimiter error."""

from src.html2typst import translate_html_to_typst

# The HTML from the problem statement
html = """<p style="text-align: center;"><strong>UCHsdfadsfasfas2</strong></p>
<p style="text-align: center;"><strong>&nbsp;</strong></p>
<p style="text-align: center;"><strong>właściciefdsafsafas
    </strong><strong style="color: black;">127</strong><strong> we Wrodsafdsafdsmości na rok 2022.</strong></p>
<p style="text-align: justify;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: justify;"><span style="color: black;">Działadsfsafdsafas następuje:</span></p>
<p style="text-align: center;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: center;"><span style="color: black;">§1</span></p>
<p style="text-align: justify;"><span style="color: black;">Przyjsfdsafdsafsadr 1 do Uchwały.</span>
</p>
<p style="text-align: center;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: center;"><span style="color: black;">§2</span></p>
<p style="text-align: justify;"><span style="color: black;">Ustfsdafasdj, która wynosi </span><strong>2,30 zasdfasfsdał/m2</strong><span style="color: black;"> powierzchni
        użytkowejdsfasfsafsokości </span><strong style="color: black;">27,00
        zł/udział</strong><span style="color: black;">*.</span></p>
<ul>
    <li style="text-align: justify;">zaliczkfsdfdsafa
        garażfsdafdasynosi <strong>1324342,00 zł</strong> od jednego stanowiska.</li>
    <li style="text-align: justify;">zaliczkfsdafsafash
        wynosi <strong>3242420 zł</strong> od fdasfa.</li>
</ul>
<p style="text-align: center;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: center;"><span style="color: black;">§3</span></p>
<p style="text-align: justify;"><span style="color: black;">Przyjmują wysokośćsdfasfasfet zużycia
        energii cieplnej (C.C.W</span></p>
<p style="text-align: justify;"><span style="color: black;"> &nbsp;i C.O.), wody i fasdfasfas
        wysokości:</span></p>
<p style="text-align: justify;"><span style="color: black;">• Zużycifsdafasfasfycie (w danym lokalu) </span></p>
<p style="text-align: justify;"><span style="color: black;"> z popgfdgssdfwego.</span></p>
<p style="text-align: justify;"><span style="color: black;">&nbsp;- Woda zfsdgg ścieków: </span><strong
        style="color: black;">324242,80 zł/m3</strong></p>
<p style="text-align: justify;"><span style="color: black;">&nbsp;- Podgrzew wody: </span><strong
        style="color: black;">17,423424 zł/m3</strong></p>
<p style="text-align: justify;"><span style="color: black;">&nbsp;- Centralne ogrzewanie:&nbsp;</span><strong
        style="color: black;">3,30&nbsp;zł/m2</strong><span style="color: black;">&nbsp;pow. użytk.</span></p>
<p style="text-align: center;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: center;"><span style="color: black;">§4</span></p>
<p style="text-align: justify;"><span style="color: black;">Wysokość pasdffafsadf
        może ulec zmianie, </span></p>
<p style="text-align: justify;"><span style="color: black;">w zwiąasdfsafdasfaokości nowych zaliczek, bez konieczności
        podejmowania nowej uchwały w tej sprawie. </span></p>
<p style="text-align: center;"><span style="color: black;">§5</span></p>
<p style="text-align: justify;"><span style="color: black;">Upoważnfsdafdsafasfnu gospodarczego. </span></p>
<p style="text-align: center;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: center;"><span style="color: black;">§6</span></p>
<p style="text-align: justify;"><span style="color: black;">Wysokości fdasfsafu gospodarczego. </span></p>
<p style="text-align: center;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: center;"><span style="color: black;">§7</span></p>
<p style="text-align: justify;"><span style="color: black;">Właściciefsdafasejszej uchwały.</span></p>
<p style="text-align: center;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: justify;"><span style="color: black;">&nbsp;</span></p>
<p style="text-align: justify;"><span style="color: black;">* w skład kosztówfdasfasfsafasfas 19.03.2010 r.</span></p>
<p><br></p>"""

try:
    result = translate_html_to_typst(html)
    print("Success! Generated Typst:")
    print("=" * 80)
    print(result)
    print("=" * 80)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
