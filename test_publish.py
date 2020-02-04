import json
import sys
import base64
from mock import patch, call
import publish
import utils
from version import __version__


def test_invoke_help():
    old_argv = sys.argv
    sys.argv = ['publish', '-test']
    # invoke as script
    utils.execute_module('__main__', 'publish.py')
    sys.argv = old_argv


@patch('publish.execute_shell')
def test_check_for_uncommitted_files(execute_shell_mock):
    execute_shell_mock.return_value = 'nothing to commit'
    publish.check_for_uncommitted_files()


@patch('publish.execute_shell')
def test_check_for_uncommitted_files_raises_error(execute_shell_mock):
    execute_shell_mock.return_value = 'asdf'
    try:
        publish.check_for_uncommitted_files()
        assert False, 'expecting ValueError'
    except ValueError as e:
        assert 'uncommitted' in '\n'.join(e.args)


@patch('publish.execute_shell')
def test_create_version_tag_and_push(execute_shell_mock):
    publish.create_version_tag_and_push('asdf')
    calls = [
        call(['git', 'tag', 'asdf']),
        call(['git', 'push', 'origin', 'HEAD', '--tags'])
    ]
    execute_shell_mock.assert_has_calls(calls)


@patch('urllib.request.urlretrieve')
def test_download_tar(urllib_urlretrieve_mock):
    filename = 'asdf'
    publish.download_tar(filename)
    calls = [
        call('https://github.com/clintmod/macprefs/archive/' + filename, filename),
    ]
    urllib_urlretrieve_mock.assert_has_calls(calls)


@patch('publish.execute_shell')
def test_calc_sha256(execute_shell_mock):
    filename = 'asdf'
    execute_shell_mock.return_value = 'sha'
    asdf = publish.calc_sha256(filename)
    assert asdf == 'sha'
    calls = [
        call(['shasum', '-a', '256', filename])
    ]
    execute_shell_mock.assert_has_calls(calls)


def test_create_brew_formula_file_content():
    filedata = publish.create_brew_formula_file_content('ver1', 'asdf1234')
    filedata = base64.b64decode(filedata).decode('utf-8')
    assert 'ver1.tar.gz' in filedata
    assert 'sha256 "asdf1234"' in filedata


@patch('publish.urllib.request.urlopen')
@patch('publish.json.load')
def test_get_sha_of_old_macprefs_formula(json_load_mock, urlopen_mock):
    json_load_mock.return_value = {'sha': 'asdf'}
    sha = publish.get_sha_of_old_macprefs_formula()
    urlopen_mock.assert_called_with(
        'https://api.github.com/repos/clintmod/homebrew-formulas/contents/Formula/macprefs.rb')
    assert sha == 'asdf'


@patch('publish.open')
@patch('publish.execute_shell')
# pylint: disable=unused-argument
def test_upload_new_brew_formula(execute_shell_mock, open_mock):
    execute_shell_mock.return_value = 'Status: 200 OK'
    data = publish.upload_new_brew_formula('asdf', 'ver1', 'sha1')
    json.loads(data)
    open_mock.assert_called_once()
    # pylint: disable=unused-variable
    args, kwargs = execute_shell_mock.call_args
    assert 'curl' in args[0]
    assert 'https://api.github.com/repos/clintmod/homebrew-formulas/contents/Formula/macprefs.rb' in args[0]

@patch('publish.verify_macprefs')
@patch('publish.download_macprefs')
@patch('publish.cleanup')
@patch('publish.upload_new_brew_formula')
@patch('publish.get_sha_of_old_macprefs_formula')
@patch('publish.create_brew_formula_file_content')
@patch('publish.calc_sha256')
@patch('publish.download_tar')
@patch('publish.create_version_tag_and_push')
@patch('publish.check_for_uncommitted_files')
# pylint: disable=R0913
def test_main(check_commits_mock, create_version_mock,
              download_tar, calc_sha256_mock,
              create_brew_mock, get_sha_mock,
              upload_mock, cleanup_mock,
              download_mock, verify_mock):
    assert publish.main()
    check_commits_mock.assert_called_once()
    create_version_mock.assert_called_once()
    download_tar.assert_called_once()
    calc_sha256_mock.assert_called_once()
    create_brew_mock.assert_called_once()
    get_sha_mock.assert_called_once()
    upload_mock.assert_called_once()
    cleanup_mock.assert_called_once()
    download_mock.assert_called_once()
    verify_mock.assert_called_once()


@patch('publish.execute_shell')
def test_download_macprefs(execute_shell_mock):
    publish.download_macprefs()
    execute_shell_mock.assert_called_with(
        ['brew', 'upgrade', 'macprefs'], False, '.', True)


@patch('publish.execute_shell')
def test_verify_macprefs(execute_shell_mock):
    execute_shell_mock.return_value = __version__
    publish.verify_macprefs()
    execute_shell_mock.assert_called_with(['macprefs', '--version'])


@patch('publish.execute_shell')
def test_verify_macprefs_throws_assertion_error(execute_shell_mock):
    execute_shell_mock.return_value = 'asdf'
    try:
        publish.verify_macprefs()
        assert False, 'expected AssertionError'
    except AssertionError as e:
        execute_shell_mock.assert_called_with(['macprefs', '--version'])
        assert __version__ in '\n'.join(e.args)


@patch('publish.glob.glob')
@patch('publish.os.remove')
def test_cleanup_removes_tar_gz_files(remove_mock, glob_mock):
    glob_mock.return_value = 'a'
    publish.cleanup()
    assert call('a') in remove_mock.mock_calls
    assert call('github_request.json') in remove_mock.mock_calls
