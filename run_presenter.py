"""
Runs the Flask-based webserver.
"""
import sys

if __name__ == '__main__':
    try:
        if sys.argv[1] == "prod":
            from presenter import run_prod

            run_prod()

        elif sys.argv[1] == "dev":
            from presenter import run_dev

            run_dev()

        else:
            raise IndexError

    except IndexError:
        sys.exit("Argument must be either 'prod' or 'dev'!")
