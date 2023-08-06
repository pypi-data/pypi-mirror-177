from collections import namedtuple
import platform as pf

OSPlatform = namedtuple("OSPlatform", ("os", "arch", "bits"))


def oskind(osname):
    """
    Parse system architecture kind.

    Args:
    - osname: `str` - architecture name

    Returns: `str` - parsed architecture name
    """
    if osname.startswith("arm") or osname.startswith("aarch"):
        # armv7(32), armv8(64), aarch64, arm64, ...
        return "arm"
    elif "86" in osname or osname == "amd64":
        # x86, i386, i686, x86_64, amd64
        return "x86"
    elif osname.startswith("ppc"):
        return "powerpc"
    elif osname.startswith("mips"):
        return "mips"
    elif "riscv" in osname:
        return "riscv"
    elif osname.startswith("sparc"):
        return "sparc"
    elif osname.startswith("loong"):
        return "loongarch"
    return osname


def osbits(osname):
    """
    Parse system architecture bits.

    Args:
    - osname: `str` - architecture name

    Returns: `int` - parsed architecture bits
    """
    if "64" in osname:
        return 64
    elif osname.startswith("armv8"):
        return 64
    elif osname == "s390x":
        return 64
    else:
        return 32


def osplatform():
    """
    Get system platform info.

    Returns: `OSPlatform` - parsed platform info
    """
    system, machine = pf.system(), pf.machine()
    return OSPlatform(system, oskind(machine), osbits(machine))
