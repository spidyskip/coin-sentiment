import argparse


def main():
    parser = argparse.ArgumentParser(description="Cli tool")
    parser.add_argument("--version", action="version", version=f"{__name__} 1.0")

    args = parser.parse_args()
    if args.version:
        package_version = "1.0"
        print("Version: {}".format(package_version))


if __name__ == "__main__":
    main()
