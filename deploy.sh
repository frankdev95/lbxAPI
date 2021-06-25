#!/bin/bash

ssh root@46.101.52.87 'rm -r ~/LBX/lbxAPI'
scp -r ../lbxAPI root@46.101.52.87:~/LBX
ssh root@46.101.52.87 'docker stop lbx-api'
ssh root@46.101.52.87 'docker rm lbx-api'
ssh root@46.101.52.87 'docker build -t lbx-api-image ~/LBX/lbxAPI'
ssh root@46.101.52.87 'docker run --name lbx-api -d -e PORT="3000" -e PRODUCTION=True -p 3000:3000 lbx-api-image'
ssh root@46.101.52.87 'docker logs -f lbx-api'
