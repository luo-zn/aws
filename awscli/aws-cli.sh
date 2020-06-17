#!/bin/bash
#Created By lzn


function  awsCli()
{
  docker run --rm  -it -v $AWS_CONFIG:/root/.aws -v $(pwd):$(pwd) -w $(pwd) jenner/awscli  aws  $* 
}
function initCfg(){  
  export AWS_CONFIG=$(pwd)/aws-configure
  if [ ! -d $AWS_CONFIG ];then
    echo "Init AWS CONFIG!"
    mkdir -p $AWS_CONFIG
  fi
  if [ ! -f $AWS_CONFIG/config ];then
cat > $AWS_CONFIG/config << EOF
[default]
region = eu-central-1
EOF
  fi
  
  if [ ! -f  $AWS_CONFIG/credentials ];then
    cat > $AWS_CONFIG/credentials << EOF
[default]
aws_access_key_id = change_this_value
aws_secret_access_key = change_this_value
EOF
fi
}

if [ ! -n "$AWS_CONFIG" ];then
  echo "AWS_CONFIG does not exist!"
  initCfg
fi
awsCli $*
