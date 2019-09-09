@echo off

pushd %CD%
cd /d "server"
start gameserver.bat .\map_r2m1.txt 127.0.0.1 6001 
popd

pushd %CD%
cd /d "Client_Python\client"
start python -m ballclient.main 2222 127.0.0.1 6001
popd

rem sleep 2s
ping -n 2 127.0.0.1>null

pushd %CD%
cd /d "ai"
start gameclient.bat 1111 127.0.0.1 6001
popd



rem sleep 30s
ping -n 30 127.0.0.1>null

pushd %CD%
cd /d "ui"
start nw.bat
popd
