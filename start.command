#!/bin/sh
cd "$( dirname "$0" )"
java -Xms1G -Xmx4G -XX:+UseG1GC -jar spigot.jar nogui
