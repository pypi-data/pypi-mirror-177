import sys, os
import biorun.libs.placlib as plac

URL = "http://data.biostarhandbook.com/make/code.tar.gz"

@plac.flg('overwrite', "overwrite existing files", abbrev="o")
def run(overwrite=False):
    """
    Downloads the data from the URL.
    """
    import requests
    import tarfile
    import io

    # Download the data.
    resp = requests.get(URL)
    resp.raise_for_status()

    # Extract the data.
    tar = tarfile.open(fileobj=io.BytesIO(resp.content))


    # Flags each tarinfo for extraction
    def check_file(tarinfo):
        return os.path.isfile(tarinfo.name), tarinfo

    pairs = list(map(check_file, tar))
    pairs = list(filter(lambda x: x[1].isfile(), pairs))

    found = filter(lambda x: x[0], pairs)
    found = list(map(lambda x: x[1], found))

    not_found = filter(lambda x: not x[0], pairs)
    not_found = list(map(lambda x: x[1], not_found))

    for tf in found:
        if overwrite:
            print(f"# overwriting: {tf.name}")
            tar.extract(member=tf)
        else:
            print(f"# skipping: {tf.name}")

    # Unpack all not found files.
    for tf in not_found:
        print(f"# creating: {tf.name}")
        tar.extract(member=tf)

    if not_found:
        print(f"# created {len(not_found)} files.")

    if found:
        if not overwrite:
            print(f"# {len(found)} files already exist.")
            print(f"# use -o to overwrite existing files")
        else:
            print(f"# {len(found)} files were overwritten")


def main():
    """
    Entry point for the script.
    """
    plac.call(run)

if __name__ == '__main__':
    main()
