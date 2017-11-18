from mock import patch, call
import publish


@patch("publish.raw_input")
def test_prompt_for_version(raw_input_mock):
    publish.prompt_for_version()
    raw_input_mock.assert_called_once()


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


def test_get_sha_of_old_macprefs_formula():
    sha = publish.get_sha_of_old_macprefs_formula()
    assert sha is not None


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


@patch("publish.cleanup")
@patch("publish.upload_new_brew_formula")
@patch("publish.get_sha_of_old_macprefs_formula")
@patch("publish.create_brew_formula_file_content")
@patch("publish.calc_sha256")
@patch("publish.download_tar")
@patch("publish.create_version_tag_and_push")
@patch("publish.prompt_for_version")
# pylint: disable=unused-argument
# pylint: disable=R0913
def test_main(prompt_mock, create_version_mock, download_tar,
              calc_sha256_mock, create_brew_mock, get_sha_mock, upload_mock,
              cleanup_mock):
    assert publish.main()
