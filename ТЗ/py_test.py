import io
import sys
import pytest
from read_csv import calculate_median, main


def test_single_student():
    csv_data = """student,coffee_spent
Алиса,10
Алиса,20
Алиса,30
"""
    file = io.StringIO(csv_data)

    result = calculate_median([file])

    assert result == [["Алиса", 20.0]]


def test_multiple_students():
    csv_data = """student,coffee_spent
Алиса,10
Глеб,30
Алиса,20
Глеб,10
"""
    file = io.StringIO(csv_data)

    result = calculate_median([file])

    assert ["Алиса", 15.0] in result
    assert ["Глеб", 20.0] in result


def test_sorting_by_median():
    csv_data = """student,coffee_spent
Алиса,10
Алиса,20
Глеб,50
Глеб,60
"""
    file = io.StringIO(csv_data)

    result = calculate_median([file])

    assert result[0][0] == "Глеб"


def test_multiple_files():
    csv1 = io.StringIO("""student,coffee_spent
Алиса,10
""")

    csv2 = io.StringIO("""student,coffee_spent
Алиса,30
""")

    result = calculate_median([csv1, csv2])

    assert result == [["Алиса", 20.0]]


def test_cli_output(tmp_path, capsys):
    csv_file = tmp_path / "data.csv"

    csv_file.write_text(
        "student,coffee_spent\n"
        "Алиса,10\n"
        "Алиса,20\n"
        "Глеб,30\n"
    )

    sys.argv = [
        "read_csv.py",
        "--files",
        str(csv_file),
        "--report",
        "median-coffee"
    ]

    main()

    captured = capsys.readouterr()

    assert "student" in captured.out
    assert "median_coffee" in captured.out
    assert "Алиса" in captured.out