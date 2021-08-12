import os
import subprocess
import posixpath


def generate_patch_file(target):
    subprocess.call(['git', 'fetch', 'origin', target])
    old_patch = subprocess.check_output(['git', 'format-patch', f'origin/{target}', 'fld/.', '-o', 'patches'])
    old_patch = old_patch.decode('utf-8')

    patch_path = os.path.dirname(old_patch)
    patch_file = os.path.basename(old_patch)

    split = patch_file.split('-')
    patch_file = ''.join(split[1:])
    new_patch = posixpath.join(patch_path, patch_file)

    os.rename(old_patch.rstrip('\n'), new_patch.rstrip('\n'))

    with open('patches/.patches', 'r+') as f:
        lines = f.readlines()
        lines.insert(0, patch_file)
        f.seek(0)
        f.writelines(lines)

    return new_patch


def main():
    parent_branch = os.environ["INPUT_PARENT_BRANCH"]

    out_patch_file = generate_patch_file(parent_branch)
    print(f"::set-output name=out_patch_file::{out_patch_file}")


if __name__ == "__main__":
    main()
