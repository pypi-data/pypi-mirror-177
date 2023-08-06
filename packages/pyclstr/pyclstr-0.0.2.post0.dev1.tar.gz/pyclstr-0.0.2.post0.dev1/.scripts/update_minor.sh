
# meant to be run in root directory

read major minor patch <<< $(bash .scripts/get_version.sh)
minor=$(expr $minor + 1)
git tag ${major}.${minor}.0


