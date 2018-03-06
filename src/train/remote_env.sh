#!/bin/bash
export JAVA_HOME=/usr/lib/jvm/java-1.7.0                                                                                                                   
export HADOOP_PREFIX=/usr/local/hadoop-2.7.2                                                                                                               
export HADOOP_HOME=$HADOOP_PREFIX                                                                                                                          
                                                                                                                                                           
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HADOOP_PREFIX/lib/native:$JAVA_HOME/lib/amd64/server:/usr/local/cuda-8.0/lib64/:$HOME/.local/lib/:$LD_LIBRARY_PATH 
