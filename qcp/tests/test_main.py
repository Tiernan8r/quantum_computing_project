from qcp import main


def test_main():
    try:
        main.main()
    except Exception:
        assert False, "main() raised an exception."


if __name__ == '__main__':
    test_main()
