""" Bottie bot """
__version__ = "2023.6.dev"

if "dev" in __version__:
    from pathlib import Path

    try:
        import subprocess

        bottie_basedir = Path(__file__).parent

        __version__ = (
            __version__
            + "-"
            + subprocess.check_output(
                ["git", "log", '--format="%h"', "-n 1"],
                stderr=subprocess.DEVNULL,
                cwd=bottie_basedir,
            )
            .decode("utf-8")
            .rstrip()
            .strip('"')
        )

    except Exception:  # pragma: no cover
        # git not available, ignore
        pass
