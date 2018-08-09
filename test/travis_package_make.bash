#!/bin/bash -xve

#ワークスペースにリポジトリをコピー
rsync -av ./ ~/catkin_ws/src/pimouse_run_corridor/

#pimouse_rosをgit cloneでワークスペースに持ってくる
cd ~/catkin_ws/src/
git clone --depth=1 https://github.com/citueda/pimouse_ros.git
        #↑depth=1を指定すると最新のものだけクローンできる

cd ~/catkin_ws
catkin_make
