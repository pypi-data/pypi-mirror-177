
# meant to be run in root directory

read major minor patch <<< $(bash .scripts/get_version.sh)
major=$(expr $major + 1)
git tag ${major}.0.0


