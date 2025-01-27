
"""
Convert ACE neutron files to OpenMC HDF5 and register them
in the cross_sections.xml library.
"""

def main():

    from pathlib import Path
    reporoot = Path(__file__).parent
    ace_datadir = reporoot.joinpath('ace')
    h5outdir = reporoot.joinpath('tmp_conv_data')
    outxml = reporoot.joinpath('cross_sections.xml')
    assert ace_datadir.is_dir()

    ace_files = sorted( ace_datadir.glob('*.ace') )
    assert len(ace_files) >= 4

    import openmc
    openmc_datalib = openmc.data.DataLibrary()

    def is_force():
        import sys
        return ( '--force' in sys.argv[1:]
                 or '-f' in sys.argv[1:] )

    if outxml.exists():
        if is_force():
            print(f"--force: Removing existing {outxml}")
            outxml.unlink()
        else:
            raise SystemExit('ERROR: file already exists (run with'
                             f' --force/-f to remove it): {outxml}')

    if h5outdir.is_dir():
        if is_force():
            print(f"--force: Removing existing {h5outdir}")
            import shutil
            shutil.rmtree(h5outdir)
        else:
            raise SystemExit('ERROR: directory already exists (run with'
                             f' --force/-f to remove it): {h5outdir}')
    h5outdir.mkdir()
    for f_ace in ace_files:
        # Convert to HDF5 and register data file
        f_h5 = h5outdir.joinpath( '%s.h5'%f_ace.stem )
        assert not f_h5.is_file() and f_h5.parent.is_dir()
        openmc.data.IncidentNeutron.from_ace(f_ace).export_to_hdf5(f_h5)
        print(f"Generated {f_h5}")
        openmc_datalib.register_file(f_h5)

    openmc_datalib.export_to_xml(outxml)
    assert outxml.is_file()
    print(f"Generated {outxml}")

if __name__ == '__main__':
    main()
