#!/usr/bin/env python3
# Austin Varghese
# 1098759
# CIS*4010
# Assignment 1 - WS S3 Storage Shell (S5)

#
#  Libraries and Modules
#
import configparser
import os 
import sys 
import pathlib
import boto3
import s3Functions as s3f

#
#  Find AWS access key id and secret access key information
#  from configuration file
#
config = configparser.ConfigParser()
config.read("S5-S3.conf")
aws_access_key_id = config['default']['aws_access_key_id']
aws_secret_access_key = config['default']['aws_secret_access_key']

try:
#
#  Establish an AWS session
#
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
#
#  Set up client and resources
#
    s3 = session.client('s3')
    s3_res = session.resource('s3')

    s3.list_buckets()

    print ( "Welcome to the AWS S3 Storage Shell (S5)" )
    print ( "You are now connected to your S3 storage" )
    print ( "You have all the functionality of your local terminal with the S3 resource" )

    # 
    # ******SHELL SCRIPT*******
    # 

    # variable that will store what the current working directory is for relative pathing

    cwlocn = "/" # formatting for cwlocn will be: /bucket/folder only if it has been changed, keep it blank


    arg = ""
    while (arg != "quit" and arg != "exit"):   
        
        arg = input("S5> ")

        args = arg.split(" ")

        if args[0] == "help":
            print("List of S3 Shell Commands")
            print("\tcreate_bucket")
            print("\tdelete_bucket")
            print("\tcreate_folder")
            print("\tlist (-l)")
            print("\tcwlocn")
            print("\tchlocn")
            print("\tlocs3cp")
            print("\ts3loccp")
            print("\ts3copy")
            print("\ts3delete")

        # ******** S3 COMMANDS ********
        
        # 
        # Local File Functions
        # 

        # copy local file to Cloud location [completed]
        elif args[0] == "locs3cp":

            # args[1] has to be a local file
            # args[2] has to be a new s3 object with the pathing of where it is and its new file name with correct suffix (.jpg)

            if len(args) != 3 or pathlib.PurePath(args[1]).suffix != pathlib.PurePath(args[2]).suffix:
                print("error, incorrect format! \ntry: \n\tlocs3cp <full or relative pathname of local file> /<bucket name>/<full pathname of S3 object>")

            else:   

                localFile = args[1]
                s3Path = args[2]

                ret = s3f.locs3cp(s3, s3_res, localFile,s3Path, cwlocn)

                # this works
                # response = s3.upload_file(localFile, 'cis4010-avargh01-test2-s3', 'test/folder/' + fileName)
                # ret = s3f.local_to_s3_copy( s3 , localFile, bucketName, s3FilePath )
                
        # copy Cloud object to local file system
        elif args[0] == "s3loccp":

            if len(args) != 3 or pathlib.PurePath(args[1]).suffix != pathlib.PurePath(args[2]).suffix:
                print("error, incorrect format! \ntry: \n\ts3loccp /<bucket name>/<full / relative pathname of S3 object> <full or relative pathname of the local file>")

            else:            
                s3Path = args[1]
                localFile = args[2]

                ret = s3f.s3loccp(s3, s3_res, localFile, s3Path, cwlocn)
              
        # 
        # Cloud Functions
        # 

        # create bucket [completed]

        elif args[0] == "create_bucket":
            if len(args) != 2 or args[1][0] != "/":
                print("error, incorrect format! \ntry: \n\tcreate_bucket /<bucket name>")

            else:
                bucketName = args[1][1:]
                # print(bucketName)
                ret = s3f.bucket_create( s3, bucketName )

        # change directory
        elif args[0] == "chlocn":
            if len(args) != 2 or pathlib.PurePath(args[1]).suffix != "":
                print("error, incorrect format! \ntry: ")
                print("\tchlocn /<bucket name> \n\tchlocn /<bucket name>/<full pathname of directory> \n\tchlocn <full or relative pathname of directory>")

            else:
                s3Path = args[1]
                
                cwlocn = s3f.chlocn(s3, s3_res, s3Path, cwlocn)


        # create directory / folder
        # you should be able to create folders relatively with chlocn as well as with the full path name (if relative then must error check cwlocn)
        elif args[0] == "create_folder":
            
            if len(args) != 2 or pathlib.PurePath(args[1]).suffix != "":
                print("error, incorrect format! \ntry: ")
                print("\tcreate_folder /<bucket name>/<full pathname for the folder> \n\tcreate_folder <full or relative pathname for the folder>")

            else:

                s3Path = args[1]

                try:

                    ret = s3f.create_folder(s3, s3_res, s3Path, cwlocn)

                except:
                    print("error, could not create folder\ntry: ")
                    print("\tcreate_folder /<bucket name>/<full pathname for the folder> \n\tcreate_folder <full or relative pathname for the folder>")

        # current working directory / location [completed]
        elif args[0] == "cwlocn":
            if len(args) != 1:
                print("error, incorrect format! \ntry: ")
                print("\tcwlocn")

            else:

                # cwlocn function (should only print / if cwlocn == "")
                print(""+cwlocn)

        # list buckets, directories, objects
        elif args[0] == "list":

            s3Path = cwlocn

            long = False

            # list cwlocn
            if len(args) == 1:
                s3Path = cwlocn
                ret = s3f.s3List(s3, s3_res, s3Path, cwlocn, long)

            # list long cwlocn
            elif len(args) == 2 and args[1] == "-l":
                long = True
                s3Path = cwlocn
                ret = s3f.s3List(s3, s3_res, s3Path, cwlocn, long)

            # list inputted path
            elif len(args) == 2 and args[1] != "-l":
                s3Path = args[1]
                ret = s3f.s3List(s3, s3_res, s3Path, cwlocn, long)

            # list long inputted path
            elif len(args) == 3 and args[1] == "-l":
                long = True
                s3Path = args[2]
                ret = s3f.s3List(s3, s3_res, s3Path, cwlocn, long)

            else:
                print("try: \n\tlist\n\tlist /<bucket>/path")

            if ret == 1:
                print("try: \n\tlist\n\tlist /<bucket>/path")
            

        # copy objects
        elif args[0] == "s3copy":
            if len(args) != 3 or pathlib.PurePath(args[1]).suffix != pathlib.PurePath(args[2]).suffix:
                print("error, incorrect format! \ntry: ")
                print("\tS3copy <from S3 location of object> <to S3 location>")

            else:
                # copy objects function
                s3source = args[1]
                s3dest = args[2]

                ret = s3f.s3copy(s3, s3_res, s3source, s3dest, cwlocn)


        # delete objects
        elif args[0] == "s3delete":
            if len(args) != 2:
                print("error, incorrect format! \ntry: ")
                print("\ts3delete <full or indirect pathname of object>")

            else:
                # delete objects function
                s3Path = args[1]

                ret = s3f.s3delete(s3, s3_res, s3Path, cwlocn)

        # delete objects
        elif args[0] == "delete_bucket":
            if len(args) != 2 or args[1][0] != "/":
                print("error, incorrect format! \ntry: ")
                print("\tdelete_bucket /<bucket name>")

            else:
                # delete bucket function
                bucketName = args[1][1:]

                ret = s3f.delete_bucket(s3, bucketName)

                

        # BASH COMMANDS
        elif args[0] == "cd":

            if len(args) == 2:
                try:
                    cwd = os.getcwd()
                    os.chdir(args[1])
                    cwd = os.getcwd()
                    print("Changed directory: ", cwd)
                except:
                    print("error, cannot change local directory")
            else:
                print("try: \n\t cd <full/relative local path>")
                
        else:
            os.system(arg)
except:
    print ( "Welcome to the AWS S3 Storage Shell (S5)" )
    print ( "You could not be connected to your S3 storage" )
    print ( "Please review procedures for authenticating your account on AWS S3" )
