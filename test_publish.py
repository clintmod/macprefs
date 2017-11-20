import sys
import imp
from mock import patch, call
import publish
from version import __version__

def test_invoke_help():
    old_argv = sys.argv
    sys.argv = ['publish', '-test']
    # invoke as script
    imp.load_source('__main__', 'publish.py')
    sys.argv = old_argv


@patch("publish.execute_shell")
def test_create_version_tag_and_push(execute_shell_mock):
    publish.create_version_tag_and_push('asdf')
    calls = [
        call(['git', 'tag', 'asdf']),
        call(['git', 'push', '--tags'])
    ]
    execute_shell_mock.assert_has_calls(calls)


@patch("urllib.urlretrieve")
def test_download_tar(urllib_urlretrieve_mock):
    filename = "asdf"
    publish.download_tar(filename)
    calls = [
        call('https://github.com/clintmod/macprefs/archive/' + filename, filename),
    ]
    urllib_urlretrieve_mock.assert_has_calls(calls)


@patch("publish.execute_shell")
def test_calc_sha256(execute_shell_mock):
    filename = 'asdf'
    execute_shell_mock.return_value = "sha"
    asdf = publish.calc_sha256(filename)
    assert asdf == "sha"
    calls = [
        call(['shasum', '-a', '256', filename])
    ]
    execute_shell_mock.assert_has_calls(calls)


def test_create_brew_formula_file_content():
    filedata = publish.create_brew_formula_file_content("ver1", "asdf1234")
    filedata = filedata.decode('base64')
    assert 'ver1.tar.gz' in filedata
    assert 'sha256 "asdf1234"' in filedata


@patch("publish.urllib2.urlopen")
@patch("publish.json.load")
def test_get_sha_of_old_macprefs_formula(json_load_mock, urlopen_mock):
    json_load_mock.return_value = {"sha":"asdf"}
    sha = publish.get_sha_of_old_macprefs_formula()
    urlopen_mock.assert_called_with('https://api.github.com/repos/clintmod/homebrew-formulas/contents/Formula/macprefs.rb')
    assert sha == "asdf"


@patch("publish.open")
@patch("publish.execute_shell")
# pylint: disable=unused-argument
def test_upload_new_brew_formula(execute_shell_mock, open_mock):
    publish.upload_new_brew_formula("asdf", "ver1", "sha1")
    open_mock.assert_called_once()
    # pylint: disable=unused-variable
    args, kwargs = execute_shell_mock.call_args
    assert 'curl' in args[0]
    assert 'https://api.github.com/repos/clintmod/homebrew-formulas/contents/Formula/macprefs.rb' in args[0]


@patch("publish.os.remove")
def test_cleanup(remove_mock):
    publish.cleanup()
    assert remove_mock.call_count > 0

@patch("publish.verify_macprefs")
@patch("publish.download_macprefs")
@patch("publish.cleanup")
@patch("publish.upload_new_brew_formula")
@patch("publish.get_sha_of_old_macprefs_formula")
@patch("publish.create_brew_formula_file_content")
@patch("publish.calc_sha256")
@patch("publish.download_tar")
@patch("publish.create_version_tag_and_push")
# pylint: disable=unused-argument
# pylint: disable=R0913
def test_main(create_version_mock, download_tar,
              calc_sha256_mock, create_brew_mock, get_sha_mock, upload_mock,
              cleanup_mock, download_mock, verify_mock):
    assert publish.main()

@patch("publish.execute_shell")
def test_download_macprefs(execute_shell_mock):
    publish.download_macprefs()
    execute_shell_mock.assert_called_with(['brew', 'upgrade', 'macprefs'], False, '.', True)

@patch("publish.execute_shell")
def test_verify_macprefs(execute_shell_mock):
    execute_shell_mock.return_value = __version__
    publish.verify_macprefs()
    execute_shell_mock.assert_called_with(['macprefs', '--version'])

@patch("publish.execute_shell")
def test_verify_macprefs_throws_assertion_error(execute_shell_mock):
    execute_shell_mock.return_value = 'asdf'
    try:
        publish.verify_macprefs()
    except AssertionError as e:
        execute_shell_mock.assert_called_with(['macprefs', '--version'])
        assert __version__ in e.message


@patch("publish.glob.glob")
@patch("publish.os.remove")
def test_cleanup_removes_tar_gz_files(remove_mock, glob_mock):
    glob_mock.return_value = "a"
    publish.cleanup()
    assert call('a') in remove_mock.mock_calls
