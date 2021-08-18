import os
import subprocess
import posixpath


def git_setup():
    netrc_path = posixpath.join(os.environ['HOME'], '.netrc')
    git_actor = os.environ['GITHUB_ACTOR']
    git_pass = os.environ['GITHUB_TOKEN']
    with open(netrc_path, 'w') as netrc:
        netrc.writelines(['machine github.com',
                          f'login {git_actor}',
                          f'password {git_pass}',
                          'machine api.github.com',
                          f'login {git_actor}',
                          f'password {git_pass}'])

    subprocess.call(['chmod', '600', netrc_path])
    subprocess.call(['git', 'config', '--global', 'user.email', 'actions@github.com'])
    subprocess.call(['git', 'config', '--global', 'user.name', 'GitHub Action'])


def generate_patch_file(target, patch_dir, specific_folder):
    subprocess.call(['git', 'fetch', 'origin', target])
    old_patch = subprocess.check_output(['git', 'format-patch', f'origin/{target}', specific_folder, '-o', patch_dir])
    old_patch = old_patch.decode('utf-8')

    patch_path = os.path.dirname(old_patch)
    patch_file = os.path.basename(old_patch)

    split = patch_file.split('-')
    patch_file = ''.join(split[1:])
    new_patch = posixpath.join(patch_path, patch_file)

    os.rename(old_patch.rstrip('\n'), new_patch.rstrip('\n'))

    with open(f'{patch_dir}/.patches', 'r+') as f:
        lines = f.readlines()
        lines.insert(0, patch_file)
        f.seek(0)
        f.writelines(lines)

    subprocess.call(['git', 'add', f'{patch_dir}/.'])

    return new_patch


def main():
    parent_branch = os.environ["INPUT_PARENT_BRANCH"]
    patch_dir = os.environ["INPUT_PATCHES_DIR"]
    specific_folder = os.environ["INPUT_SPECIFIC_FOLDER"]

    git_setup()

    out_patch_file = generate_patch_file(parent_branch, patch_dir, specific_folder)
    print(f"::set-output name=out_patch_file::{out_patch_file}")


if __name__ == "__main__":
    main()
