def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="run Visual Sponge in debug mode", action="store_true")
    args = parser.parse_args()

    from . import MACROS
    MACROS.DEBUG_MODE = args.debug

    from .backend import run
    run()

if __name__ == "__main__":
    main()