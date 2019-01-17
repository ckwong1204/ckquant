#git stash save
git fetch --all
git checkout --force -B "origin/master"
git stash apply "stash@{0}"
