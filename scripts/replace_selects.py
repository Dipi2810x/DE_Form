import re
from pathlib import Path

files = [
    Path('c:/Users/ramju/OneDrive/Documents/DE_Form/social_sciences.html'),
    Path('c:/Users/ramju/OneDrive/Documents/DE_Form/engineering.html'),
    Path('c:/Users/ramju/OneDrive/Documents/DE_Form/mathematics.html'),
    Path('c:/Users/ramju/OneDrive/Documents/DE_Form/scientific.html'),
]

# Pattern for the numeric options block
numeric_block_re = re.compile(
    r"<select([^>]*)>\s*<option[^>]*>[^<]*</option>\s*(?:<option[^>]*>\s*0\s*</option>\s*<option[^>]*>\s*1\s*</option>\s*<option[^>]*>\s*2\s*</option>\s*<option[^>]*>\s*3\s*</option>\s*<option[^>]*>\s*4\s*</option>|(?:\s*<option[^>]*>\s*0\s*</option>\s*<option[^>]*>\s*1\s*</option>\s*<option[^>]*>\s*2\s*</option>\s*<option[^>]*>\s*3\s*</option>\s*<option[^>]*>\s*4\s*</option>))\s*</select>",
    re.IGNORECASE
)

# Pattern to detect and remove the convertSelectsToYesNo IIFE (from earlier edits)
convert_script_re = re.compile(r"\n\s*// Convert numeric 0-4 selects into Yes/No choices[\s\S]*?\}\)\(\);\s*\n", re.IGNORECASE)

yes_no_inner = "<option value=\"\" disabled selected>Select</option><option value=\"1\">Yes</option><option value=\"0\">No</option>"

for f in files:
    txt = f.read_text(encoding='utf-8')

    # Remove the conversion script if present
    txt, n_removed = convert_script_re.subn('\n', txt)
    if n_removed:
        print(f"Removed conversion script from {f.name}")

    # Replace numeric option blocks with Yes/No options
    def repl(m):
        attrs = m.group(1)
        return f"<select{attrs}>\n          {yes_no_inner}\n        </select>"

    txt_new, n_subs = numeric_block_re.subn(repl, txt)
    if n_subs == 0:
        # Try a simpler approach: replace the common repeated numeric options sequence
        txt_new = txt.replace(
            '<option value="" disabled selected>Select mark</option>\n          <option value="0">0</option>\n          <option value="1">1</option>\n          <option value="2">2</option>\n          <option value="3">3</option>\n          <option value="4">4</option>',
            '<option value="" disabled selected>Select</option>\n          <option value="1">Yes</option>\n          <option value="0">No</option>'
        )
        replaced = (txt_new != txt)
    else:
        replaced = True

    if replaced:
        f.write_text(txt_new, encoding='utf-8')
        print(f"Updated selects in {f.name} ({'regex' if n_subs else 'simple replace'})")
    else:
        print(f"No numeric option blocks found in {f.name}")

print('Done')
