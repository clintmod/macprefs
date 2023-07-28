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

FORMULA_URL = "https://api.github.com/repos/sijanc147/homebrew-formulas/contents/Formula/macprefs.rb"
TAR_URL = "https://github.com/sijanc147/macprefs/archive/{}"


def check_for_uncommitted_files():
    print("Checking for uncommitted files...")
    result = execute_shell(["git", "status"])
    if not "nothing to commit" in result:
        raise ValueError("Commit changes before publishing")


def create_version_tag_and_push(tag):
    print("Tagging git repository with version " + tag)
    execute_shell(["git", "tag", tag])
    print("Pushing the new tag to github...")
    execute_shell(["git", "push", "origin", "HEAD", "--tags"])


def download_tar(filename):
    print("Downloading the new version...")
    urllib.request.urlretrieve(TAR_URL.format(filename), filename)


def calc_sha256(filename):
    print("Calculating the sha256 of the tarball...")
    result = execute_shell(["shasum", "-a", "256", filename])
    print(result)
    sha256 = result.split("  ")[0]
    print(sha256)
    return sha256


def create_brew_formula_file_content(version, sha256):
    print("Generating base64 encoded brew formula...")
    with open("macprefs.template.rb", "r") as f:
        filedata = f.read()
    filedata = filedata.replace("###sha256###", sha256)
    filedata = filedata.replace("###version###", version)
    filedata_bytes = bytes(filedata, "utf-8")
    filedata = base64.b64encode(filedata_bytes)
    return filedata


def get_sha_of_old_macprefs_formula():
    print("Getting sha of old macprefs formula from github...")
    result = json.load(urllib.request.urlopen(FORMULA_URL))
    # print 'sha = ' + result['sha']
    return result["sha"]


def upload_new_brew_formula(content, version, sha):
    print("Uploading new formula")
    req = urllib.request.Request(
        FORMULA_URL,
        method="PUT",
        headers={
            "Authorization": f'token {os.environ["MACPREFS_TOKEN"]}',
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "path": "Formula/macprefs.rb",
                "message": f"Updating to version {version}",
                "committer": {
                    "name": "Sean B",
                    "email": "seanbugeja23@gmail.com",
                },
                "content": content.decode("utf-8"),
                "branch": "main",
                "sha": sha,
            }
        ).encode("utf-8"),
    )
    with urllib.request.urlopen(req) as response:
        result = response.read()
        if response.status != 200:
            raise ValueError("ERR", result)
    return result


def cleanup():
    print("Cleaning up...")
    for f in glob.glob("*.tar.gz"):
        os.remove(f)


def download_macprefs():
    print("Running brew update macprefs to verify version...")
    result = execute_shell(["brew", "upgrade", "macprefs"], False, ".", True)
    if not is_none_or_empty_string(result):
        print(result)


def verify_macprefs():
    result = execute_shell(["macprefs", "--version"])
    message = "\nworkspace:\t" + __version__ + "\ninstalled:\t" + result
    assert __version__ in result, message
    print("version check verified" + message)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "-test":
        return False
    version = __version__
    check_for_uncommitted_files()
    create_version_tag_and_push(version)
    filename = version + ".tar.gz"
    download_tar(filename)
    sha256 = calc_sha256(filename)
    content = create_brew_formula_file_content(version, sha256)
    sha = get_sha_of_old_macprefs_formula()
    upload_new_brew_formula(content, version, sha)
    cleanup()
    if len(sys.argv) > 1 and sys.argv[1] == "-verify":
        download_macprefs()
        verify_macprefs()
    print("Success")
    return True


if __name__ == "__main__":
    main()
