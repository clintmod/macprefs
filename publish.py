import sys
import glob
import os
import json
import urllib.request
import urllib.error
import urllib.parse
import base64
from utils import execute_shell, is_none_or_empty_string
from version import __version__


def check_for_uncommitted_files():
    print('Checking for uncommitted files...')
    result = execute_shell(['git', 'status'])
    if not 'nothing to commit' in result:
        raise ValueError(
            'There are uncommitted files in the workspace. Commit or stash them before trying to publish.')


def create_version_tag_and_push(tag):
    print('Tagging git repository with version ' + tag)
    execute_shell(['git', 'tag', tag])
    print('Pushing the new tag to github...')
    execute_shell(['git', 'push', 'origin', 'HEAD', '--tags'])


def download_tar(filename):
    print('Downloading the new version...')
    urllib.request.urlretrieve(
        'https://github.com/clintmod/macprefs/archive/' + filename, filename)


def calc_sha256(filename):
    print('Calculating the sha256 of the tarball...')
    result = execute_shell(['shasum', '-a', '256', filename])
    print(result)
    sha256 = result.split('  ')[0]
    print(sha256)
    return sha256


def create_brew_formula_file_content(version, sha256):
    print('Generating base64 encoded brew formula...')
    # Read in the file
    with open('macprefs.template.rb', 'r') as f:
        filedata = f.read()
    # Replace
    filedata = filedata.replace('###sha256###', sha256)
    filedata = filedata.replace('###version###', version)
    filedata_bytes = bytes(filedata, 'utf-8')
    filedata = base64.b64encode(filedata_bytes)
    return filedata


def get_sha_of_old_macprefs_formula():
    print('Getting sha of old macprefs formula from github...')
    result = json.load(urllib.request.urlopen(
        'https://api.github.com/repos/clintmod/homebrew-formulas/contents/Formula/macprefs.rb'))
    # print 'sha = ' + result['sha']
    return result['sha']


def upload_new_brew_formula(content, version, sha):
    print('Uploading the new macprefs formula to https://github.com/clintmod/homebrew-formulas')
    token = os.environ['MACPREFS_TOKEN']
    auth_header = 'Authorization: token ' + token
    json_header = 'Content-Type: application/json'
    data = '{"path": "Formula/macprefs.rb", "message": "Updating to version ' + version + '", '
    data += '"committer": {"name": "Clint M", "email": "cmodien@gmail.com"}, '
    data += '"content": "' + content + '", "branch": "master", "sha":"' + sha + '"}'
    with open('github_request.json', 'w') as f:
        f.write(data)
    commands = [
        'curl',
        '-i',
        '-X',
        'PUT',
        '-H',
        auth_header,
        '-H',
        json_header,
        '-d',
        '@github_request.json',
        'https://api.github.com/repos/clintmod/homebrew-formulas/contents/Formula/macprefs.rb'
    ]
    result = execute_shell(commands)
    if 'Status: 200 OK' not in result:
        raise ValueError('Error uploading new brew formula to github - result\n', result)
    return data


def cleanup():
    print('Cleaning up...')
    for f in glob.glob('*.tar.gz'):
        os.remove(f)
    os.remove('github_request.json')


def download_macprefs():
    print('Running brew update macprefs to verify version...')
    result = execute_shell(['brew', 'upgrade', 'macprefs'], False, '.', True)
    if not is_none_or_empty_string(result):
        print(result)


def verify_macprefs():
    result = execute_shell(['macprefs', '--version'])
    message = '\nworkspace:\t' + __version__ + '\ninstalled:\t' + result
    assert __version__ in result, message
    print('version check verified' + message)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-test':
        return False
    version = __version__
    check_for_uncommitted_files()
    create_version_tag_and_push(version)
    filename = version + '.tar.gz'
    download_tar(filename)
    sha256 = calc_sha256(filename)
    content = create_brew_formula_file_content(version, sha256)
    sha = get_sha_of_old_macprefs_formula()
    upload_new_brew_formula(content, version, sha)
    cleanup()
    download_macprefs()
    verify_macprefs()

    print('Success')

    return True


if __name__ == '__main__':
    main()
