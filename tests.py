import unittest
from textwrap import dedent
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def test_calculator_dot(self):
        result = get_files_info("calculator", ".")
        self.assertEqual(
            result,
            dedent(
                """\
                - tests.py: file_size=1331 bytes, is_dir=False
                - main.py: file_size=719 bytes, is_dir=False
                - pkg: file_size=4096 bytes, is_dir=True"""
            )
        )

def main():
    print("Result for current directory:")
    print(get_files_info("calculator", "."))

    print("Result for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))

    print("Result for '/bin' directory:")
    print(get_files_info("calculator", "/bin"))

    print("Result for '../' directory:")
    print(get_files_info("calculator", "../"))


if __name__ == "__main__":
    #unittest.main()
    main()