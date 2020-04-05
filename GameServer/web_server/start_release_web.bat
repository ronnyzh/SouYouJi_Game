cd srcs
set module=index
python -m bottle -s paste -b 0.0.0.0:9797 --reload %module% >>web1.log 2>&1 --debug True
pause