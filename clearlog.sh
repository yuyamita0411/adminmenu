#pycacheのフォルダを削除する。
find ./* | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
git add .
git commit -m "bk"
git push origin main