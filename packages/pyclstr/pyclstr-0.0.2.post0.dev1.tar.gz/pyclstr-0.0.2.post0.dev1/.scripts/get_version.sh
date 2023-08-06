
# meant to be run from root dir

version=$(python -c "import versioneer; print(versioneer.get_version())")
echo $version | sed 's/+.*//g' | sed 's/\./\ /g'  

