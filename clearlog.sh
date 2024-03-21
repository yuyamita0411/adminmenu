#pycacheのフォルダを削除する。
git add . && git commit -m "bk" && git push origin main &&
find ./* | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf