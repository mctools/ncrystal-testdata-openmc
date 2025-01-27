"""
Downloads ENDF-6 neutron evaluations from the IAEA repository and
converts them into ACE format using OpenMC and NJOY2016.
"""

def download_and_unzip(url, extract_to='.', check_file=None):
    import requests
    import zipfile
    import io

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    response = requests.get(url, stream=True, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes

    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        zf.extractall(extract_to)
    if check_file:
        import os
        assert os.path.isfile(check_file)

def main():

    from pathlib import Path

    reporoot = Path(__file__).parent
    ace_datadir = reporoot.joinpath('ace')

    def is_force():
        import sys
        return ( '--force' in sys.argv[1:]
                 or '-f' in sys.argv[1:] )

    if ace_datadir.is_dir():
        if is_force():
            print(f"--force: Removing existing {ace_datadir}")
            import shutil
            shutil.rmtree(ace_datadir)
        else:
            raise SystemExit('ERROR: directory already exists (run with'
                             f' --force/-f to remove it): {ace_datadir}')
    ace_datadir.mkdir()

    filenames = ('n_001-H-1_0125', 'n_001-H-2_0128', 'n_006-C-12_0625', 'n_013-Al-27_1325')

    import tempfile
    import os
    import openmc

    with tempfile.TemporaryDirectory() as tmpdir:
        for fn in filenames:
            fn_zip = Path(tmpdir).joinpath(fn + '.zip')
            fn_endf = Path(tmpdir).joinpath(fn + '.dat')
            fn_ace = ace_datadir.joinpath(fn + '.ace')
            url = 'https://www-nds.iaea.org/public/download-endf/ENDF-B-VIII.1/n/'+fn+'.zip'
            download_and_unzip(url, tmpdir, fn_endf)
            openmc.data.njoy.make_ace(fn_endf, temperatures=(293.6,), output_dir=tmpdir)
            os.rename(Path(tmpdir).joinpath('ace'), fn_ace)

if __name__ == '__main__':
    main()
