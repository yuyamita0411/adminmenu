#pycacheのフォルダを削除する。
find ./* | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
git add .
git commit -m "bk"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/adminmenu
git push origin main