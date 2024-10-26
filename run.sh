#!/bin/bash

# Check if docker engine is running
if ! docker info > /dev/null 2>&1; then
  echo "請先安裝 Docker 並確認 Docker Engine 有正常啟動"
  exit 1
fi

# environments
export COMPOSE_IGNORE_ORPHANS=True

# create volume folder if not exists
[ -d volumes ] || mkdir -p volumes/{grafana,prometheus,nginx}

# check if external network exists?
if [[ "$(docker network ls | grep "mopcon-network")" == "" ]] ; then
  docker network create mopcon-network > /dev/null 2>&1
  printf "外部網路： mopcon-network 已建立\n\n"
fi

printf "\n啟動服務：\n\n1. \e[1;31mPrometheus \e[0m (Port 9090)\n2. \e[1;32mGrafana\e[0m     (Port 3000)\n3. Nginx       (Port 8080)\n\n請選擇："

read service_name

case $service_name in

   1)
     # Prometheus
     docker-compose -f docker-compose-prometheus.yml up --build
   ;;

   2)
     # Grafana
     docker-compose -f docker-compose-grafana.yml up --build
   ;;

   3)
     # Nginx
     docker-compose -f docker-compose-nginx.yml up --build
   ;;

   *)
     printf "無效的選項\n"
   ;;
esac

exit 0
