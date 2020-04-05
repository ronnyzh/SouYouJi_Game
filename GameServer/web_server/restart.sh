id=$(ps -aux|grep python|grep index|awk '{print $2}')
kill -9 $id
echo "task $id killed"
./start_release_web.sh
echo "restart done"
