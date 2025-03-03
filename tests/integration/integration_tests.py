import subprocess

def test_correct_int_calculations():
    res = subprocess.run(
        ["./app.exe"],
        input="12+7/2",
        text=True,
        capture_output=True
    )
    assert res.returncode == 0
    assert res.stdout == "15"

def test_correct_negative_int_calculations():
    res = subprocess.run(
        ["./app.exe"],
        input="12-(5*4)",
        text=True,
        capture_output=True
    )
    assert res.returncode == 0
    assert res.stdout == "-8"

def test_correct_tricky_int_calculations():
    res = subprocess.run(
        ["./app.exe"],
        input="5-4*(8-(14/4))+16",
        text=True,
        capture_output=True
    )
    assert res.returncode == 0
    assert res.stdout == "1"

def test_correct_float_calculations():
    res = subprocess.run(
        ["./app.exe", "--float"],
        input="12+7/2",
        text=True,
        capture_output=True
    )
    assert res.returncode == 0
    assert res.stdout == "15.5000"

def test_correct_negative_float_calculations():
    res = subprocess.run(
        ["./app.exe", "--float"],
        input="12-(14)",
        text=True,
        capture_output=True
    )
    assert res.returncode == 0
    assert res.stdout == "-2.0000"

def test_correct_tricky_float_calculations():
    res = subprocess.run(
        ["./app.exe", "--float"],
        input="5-4*(8-(14/4))+14",
        text=True,
        capture_output=True
    )
    assert res.returncode == 0
    assert res.stdout == "1.0000"

def test_correct_input_symbols():
    res = subprocess.run(
        ["./app.exe"],
        input="12+221/(2)-4\n+7",
        text=True,
        capture_output=True
    )
    assert res.returncode == 0

def test_incorrect_input_symbols():
    res = subprocess.run(
        ["./app.exe"],
        input="14.5+2",
        text=True,
        capture_output=True
    )
    assert res.returncode != 0

def test_incorrect_expression():
    res = subprocess.run(
        ["./app.exe"],
        input="(45+9)+8(2+3)",
        text=True,
        capture_output=True
    )
    assert res.returncode != 0

def test_incorrect_op_order():
    res = subprocess.run(
        ["./app.exe"],
        input="31+/*7",
        text=True,
        capture_output=True
    )
    assert res.returncode != 0

def test_correct_parenthesis():
    res = subprocess.run(
        ["./app.exe"],
        input="(((322)))",
        text=True,
        capture_output=True
    )
    assert res.returncode == 0

def test_incorrect_parenthesis():
    res = subprocess.run(
        ["./app.exe"],
        input="(14))",
        text=True,
        capture_output=True
    )
    assert res.returncode != 0