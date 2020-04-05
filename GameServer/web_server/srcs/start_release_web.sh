currTime=$(date "+%Y_%m_%d")
logfile=${currTime}_mahjong.log 
python -m index  >& logs/$logfile &
