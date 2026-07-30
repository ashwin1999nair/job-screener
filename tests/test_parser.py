from parser import clean_text

def test_clean_text_removes_extra_blank_lines():
    input_text="Line 1\n\n\n\nLine 2"
    result=clean_text(input_text)
    assert result=="Line 1\n\nLine 2"

def test_clean_text_strips_whitespaces():
    input_text="  Line 1  \n  Line 2  "
    result=clean_text(input_text)
    assert result=="Line 1\nLine 2"

def test_clean_text_empty_string():
    result=clean_text("")
    assert result==""

def test_clean_text_single_line():
    result=clean_text("just one line")
    assert result=="just one line"