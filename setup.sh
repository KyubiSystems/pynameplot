module load python/gcc/27
module load gdal
module load geos
. ./venv.geo/bin/activate
export LD_LIBRARY_PATH="/cm/shared/apps/geos/3.6.1/lib:"$LD_LIBRARY_PATH
export GEOS_DIR="/cm/shared/apps/geos/3.6.1/"
