import sys
import glob
import os
import json
import urllib2
import urllib
from utils import execute_shell
from version import __version__

def create_version_tag_and_push(tag):
    print ""
    print 'Tagging git repository with version ' + tag
    execute_shell(['git', 'tag', tag])
    print ''
    print 'Pushing the new tag to github...'
    execute_shell(['git', 'push', '--tags'])


def download_tar(filename):
    print ""
    print 'Downloading the new version...'
    urllib.urlretrieve(
        'https://github.com/clintmod/macprefs/archive/' + filename, filename)


def calc_sha256(filename):
    print ""
    print 'Calculating the sha256 of the tarball...'
    result = execute_shell(['shasum', '-a', '256', filename])
    print result
    sha256 = result.split('  ')[0]
    print sha256
    return sha256


def create_brew_formula_file_content(version, sha256):
    print ""
    print 'Generating base64 encoded brew formula...'
    # Read in the file
    with open('macprefs.template.rb', 'r') as f:
        filedata = f.read()
    # Replace
    filedata = filedata.replace('###sha256###', sha256)
    filedata = filedata.replace('###version###', version)
    filedata = filedata.encode('base64').replace('\n', '')
    return filedata


def get_sha_of_old_macprefs_formula():
    print ""
    print 'Getting sha of old macprefs formula from github...'
    result = json.load(urllib2.urlopen(
        'https://api.github.com/repos/clintmod/homebrew-formulas/contents/Formula/macprefs.rb'))
    # print 'sha = ' + result['sha']
    return result['sha']


def upload_new_brew_formula(content, version, sha):
    print ""
    print 'Uploading the new macprefs formula to https://github.com/clintmod/homebrew-formulas'
    token = os.environ['MACPREFS_TOKEN']
    auth_header = 'Authorization: token ' + token
    json_header = 'Content-Type: application/json'
    data = "{\"path\": \"Formula/macprefs.rb\", \"message\": \"Updating to version "
    data += version + \
        "\", \"committer\": {\"name\": \"Clint M\", \"email\": \"cmodien@gmail.com\"}, "
    data += "\"content\": \"" + content + \
        "\", \"branch\": \"master\", \"sha\":\"" + sha + "\"}"
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
    execute_shell(commands)
    # print result


def cleanup():
    print ''
    print 'Cleaning up...'
    for f in glob.glob("*.tar.gz"):
        os.remove(f)
    os.remove('github_request.json')

def download_macprefs():
    print ''
    print 'Updating and verifying macprefs new macprefs to verify it...'
    result = execute_shell(['brew', 'upgrade', 'macprefs'], False, '.', True)
    if result is not None:
        print result

def verify_macprefs():
    result = execute_shell(['macprefs', '--version'])
    message = '\nworkspace:\t' + __version__ + '\ninstalled:\t' + result
    assert __version__ in result, message
    print 'version check verified' + message

def main():
    print 'sys.argv', sys.argv
    if len(sys.argv) > 1 and sys.argv[1] == "-test":
        return
    version = __version__
    create_version_tag_and_push(version)
    filename = version + '.tar.gz'
    download_tar(filename)
    sha256 = calc_sha256(filename)
    content = create_brew_formula_file_content(version, sha256)
    sha = get_sha_of_old_macprefs_formula()
    upload_new_brew_formula(content, version, sha)
    cleanup()
    print ''
    print 'Success'
    return True


if __name__ == '__main__':
    main()
