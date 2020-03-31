#!/bin/bash
#Created By lzn


function  awsCli()
{
  docker run -it  jenner/awscli  aws  $* 
}

awsCli $*
