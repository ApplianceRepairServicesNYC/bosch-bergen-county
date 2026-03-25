#!/usr/bin/env python3
"""
Add border wrappers to service areas and contact form sections.
"""

import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Add .sa-section-wrapper CSS if not present
    if '.sa-section-wrapper' not in content:
        content = content.replace(
            '.sa-dropdown-container {',
            '''.sa-section-wrapper {
            background: transparent;
            border: 2px solid #808080;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, .2);
            padding: 20px;
            margin: 0 auto 2rem;
            max-width: 1200px;
            box-sizing: border-box;
        }
        .sa-dropdown-container {'''
        )

    # Add service areas wrapper div if not present
    if 'class="sa-section-wrapper"' not in content:
        content = re.sub(
            r'(<section id="service-areas">)\s*(<h2)',
            r'\1\n                <div class="sa-section-wrapper">\n                \2',
            content
        )
        # Close the wrapper before </section>
        content = re.sub(
            r'(</div>\s*</div>\s*</div>)\s*(</section>\s*<section id="contact">)',
            r'\1\n                </div>\n            \2',
            content
        )

    # Add contact form wrapper if not present
    if 'id="cf-schedule-container"' not in content:
        content = re.sub(
            r'(<section id="contact">)\s*(<div class="cf-schedule-text">)',
            r'\1\n                <div id="cf-schedule-container">\n                \2',
            content
        )
        # Close the wrapper before </section> for contact
        content = re.sub(
            r'(</form>\s*</div>)\s*(</section>\s*</div>\s*</section>)',
            r'\1\n                </div>\n            \2',
            content
        )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    base_dir = '/Users/globalaffiliate/bosch-bergen-county'
    updated = 0

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in files:
            if filename.endswith('.html'):
                filepath = os.path.join(root, filename)
                if fix_file(filepath):
                    updated += 1
                    print(f"Updated: {filepath}")

    print(f"\nTotal files updated: {updated}")

if __name__ == '__main__':
    main()
