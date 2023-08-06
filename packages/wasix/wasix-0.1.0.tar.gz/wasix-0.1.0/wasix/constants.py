import os

WASIX_DIR = os.path.dirname(__file__)

# Binaries
WASIX_CC = "wasix-cc"
WASIX_CXX = "wasix-c++"
WASIX_LD = "wasix-ld"
WASIX_AR = "wasix-ar"
WASIX_NM = "wasix-nm"
WASIX_RANLIB = "wasix-ranlib"
WASIX_RUN = "wasix-run"

WASIX_CMAKE = os.path.abspath(os.path.join(WASIX_DIR, "wasix.cmake"))
