#git stash save
git reset --hard
git pull
git stash apply "stash@{0}"
