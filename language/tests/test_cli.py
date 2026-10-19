from language.neo import main


def test_cli_returns_nonzero_and_writes_runtime_error_to_stderr(tmp_path, capsys):
    source_file = tmp_path / "runtime_error.neo"
    source_file.write_text("print(unknown)", encoding="utf-8")

    exit_code = main([str(source_file)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Variable 'unknown' doesn't exist" in captured.err
    assert captured.out == ""


def test_cli_returns_nonzero_for_syntax_error(tmp_path, capsys):
    source_file = tmp_path / "syntax_error.neo"
    source_file.write_text("var = 1", encoding="utf-8")

    exit_code = main([str(source_file)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error at line:" in captured.err
    assert captured.out == ""
