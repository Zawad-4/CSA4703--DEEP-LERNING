import os, glob, sys, json

def update_repo(username, repo_name='Deep-Learning'):
    files = glob.glob('Exp*.ipynb')
    if not files:
        print('No Exp*.ipynb files found in current directory.')
        return
    for f in sorted(files, key=lambda x: int(x.replace('Exp','').replace('.ipynb','')) if x.replace('Exp','').replace('.ipynb','').isdigit() else 999):
        with open(f, 'r', encoding='utf-8') as fp:
            nb = json.load(fp)
        changed = False
        for cell in nb.get('cells', []):
            if cell.get('cell_type') == 'markdown':
                src = ''.join(cell.get('source', []))
                if 'colab.research.google.com/github/' in src:
                    old_prefix = src.split('colab.research.google.com/github/')[1].split('/blob/')[0]
                    new_prefix = f'{username}/{repo_name}'
                    if old_prefix != new_prefix:
                        src = src.replace(old_prefix, new_prefix)
                        cell['source'] = [src]
                        changed = True
        if changed:
            with open(f, 'w', encoding='utf-8') as fp:
                json.dump(nb, fp, indent=1)
            print(f'Updated {f} with {username}/{repo_name}')
        else:
            print(f'Checked {f} (already up to date)')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python update_colab_links.py <your-github-username> [optional-repo-name]')
        print('Example: python update_colab_links.py john-doe Deep-Learning')
    else:
        user = sys.argv[1]
        repo = sys.argv[2] if len(sys.argv) > 2 else 'Deep-Learning'
        update_repo(user, repo)
