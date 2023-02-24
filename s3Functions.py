#!/usr/bin/env python3
# Austin Varghese
# 1098759
# CIS*4010
# Assignment 1 - WS S3 Storage Shell (S5)

#
#  Libraries and Modules
#
import boto3
import pathlib

# helper functions
# assuming correct input

def get_bucket_name(s3Path, cwlocn):

    bucketName = "/"

    if s3Path[0] == "/":
        parents = pathlib.PurePath(s3Path).parents
        if len(parents) == 1:
            bucketName = s3Path
        else:
            bucketName = str(parents[len(parents)-2])

    else:
        parents = pathlib.PurePath(cwlocn).parents
        if len(parents) == 1:
            bucketName = cwlocn
        else:
            bucketName = str(parents[len(parents)-2])
    
    # remove leading /
    if bucketName[0] == "/":
        bucketName = bucketName[1:]
    # bucketName = bucketName[1:]

    return bucketName

# function to get path name of object in s3 without the bucket name (useful for all s3 methods)
# format: folder/some/thing.txt
def get_path(s3Path, cwlocn):

    s3FilePath = ""
    bucketName = ""
    startPath = ""

    # check if s3Path contains the initial / which indicates it is a bucket therefore the starting of the path
    if s3Path[0] == "/":
        parents = pathlib.PurePath(s3Path).parents
        if len(parents) == 1:
            bucketName = s3Path
        else:
            bucketName = str(parents[len(parents)-2])

        startPath = s3Path

    else:
        parents = pathlib.PurePath(cwlocn).parents
        if len(parents) == 1:
            bucketName = cwlocn
        else:
            bucketName = str(parents[len(parents)-2])

        startPath = cwlocn

    s3FilePath = startPath.replace(bucketName, '', 1)
    
    # if the cwlocn contains the bucket to be accessed then add s3Path (the relative path) to get the full path
    # else the s3Path is already the full path
    if startPath == cwlocn:
        s3FilePath += ("/" + s3Path)

    # need this because if you just want to access a bucket
    # you cant check if a blank string has an index at 0 or else it crashes
    # check if there is a path, if not then return blank string
    if s3FilePath == "":
        return ""

    # only remove the leading slash if not a relative path 
    if s3FilePath[0] == "/":
        s3FilePath = s3FilePath[1:]

    # print("3")
    
    return s3FilePath

# function to get the full path of the cwlocn so you can determine what directory you are currently in
def get_cwlocn(s3, s3_res, s3Path, cwlocn):
    try:

        # this needs to be able to go back and forth between directories with .. and ../.. if you are currently in something
        # / or ~ can bring you back to "home"

        if s3Path == "/" or s3Path == "~":
            return "/"

        # split the inputted path
        pathSections = (s3Path).split("/")        

        if (pathSections[0] == ''):
            newcwlocn = s3Path
            bucket = get_bucket_name(s3Path, "")
            path = get_path(s3Path, "")

            all_buckets = bucket_list(s3)

            # check if bucket exists
            if bucket in all_buckets: 
                
                # if no folder/path to find, change cwlocn to bucket
                if path == "":
                    newcwlocn = "/" + bucket
                    return newcwlocn

                else:
                    objects = object_list(s3_res, bucket)

                    if (path + "/") in objects:
                        newcwlocn = "/" + bucket + "/" + path
                        return newcwlocn
                    else:
                        # print("folder not found")
                        return cwlocn

            else:
                print("bucket not found")
                return cwlocn

        else: 

            # create a string that contains cwlocn (subject to change)
            newcwlocn = cwlocn
            dirLevel = len(newcwlocn.split("/"))
            lastPathAdded = ""

            # go through each section in inputted path
            for section in pathSections:
                # get the parents of cwlocn at begginning of for loop
                parents = pathlib.PurePath(newcwlocn).parents
                
                if dirLevel < 1: 
                    print("going back to home directory, went back too many times")
                    return "/"

                # if section has ".." then remove recent directory (with parents[0])
                if section == "..":
                    newcwlocn = str(parents[0])
                    dirLevel -= 1
                elif lastPathAdded == section:
                    continue
                # if section is not ".." then assume it is a valid bucket/folder
                else:

                    # need to check if the new cwlocn if at home, or in a bucket / folder
                    if newcwlocn == "" or newcwlocn == "/":
                        bucket = get_bucket_name("/" + section, "")
                        path = get_path("/" + section, "")
                    else:
                        bucket = get_bucket_name(newcwlocn, cwlocn)
                        path = get_path(section, newcwlocn)


                    all_buckets = bucket_list(s3)

                    # check if bucket exists
                    if bucket in all_buckets: 
                        
                        # if no folder/path to find, change cwlocn to bucket
                        if path == "":
                            dirLevel += 1
                            newcwlocn = "/" + bucket

                        else:
                            objects = object_list(s3_res, bucket)

                            if (path + "/") in objects:
                                newcwlocn = "/" + bucket + "/" + path
                                dirLevel += 1

                                lastPathAdded = path
                            else:
                                # print("folder not found")
                                return cwlocn

                    else:
                        print("bucket not found")
                        return cwlocn

            # if newcwlocn == "/":
            #     return ""
        
            return newcwlocn

    except:
        print("Cannot change directory")


def get_full_path(s3, s3_res, s3Path, cwlocn):
    try:

        # this needs to be able to go back and forth between directories with .. and ../.. if you are currently in something
        # / or ~ can bring you back to "home"

        if s3Path == "/" or s3Path == "~":
            return "/"

        # split the inputted path
        pathSections = (s3Path).split("/")   

        if (pathSections[0] == ''):
            newcwlocn = s3Path
            bucket = get_bucket_name(s3Path, "")
            path = get_path(s3Path, "")

            all_buckets = bucket_list(s3)

            # check if bucket exists
            if bucket in all_buckets: 
                
                # if no folder/path to find, change cwlocn to bucket
                if path == "":
                    newcwlocn = "/" + bucket
                    return newcwlocn

                else:
                    objects = object_list(s3_res, bucket)

                    if (path + "/") in objects:
                        newcwlocn = "/" + bucket + "/" + path
                        return newcwlocn
                    else:
                        print("folder not found")
                        return cwlocn

            else:
                print("bucket not found")
                return cwlocn

        else:      

            # create a string that contains cwlocn (subject to change)
            newcwlocn = cwlocn
            dirLevel = len(newcwlocn.split("/"))
            lastPathAdded = ""

            # go through each section in inputted path
            for section in pathSections:
                # get the parents of cwlocn at begginning of for loop
                parents = pathlib.PurePath(newcwlocn).parents
                
                if dirLevel < 1: 
                    print("going back to home directory, went back too many times")
                    return ""

                # if section has ".." then remove recent directory (with parents[0])
                if section == "..":
                    newcwlocn = str(parents[0])
                    dirLevel -= 1
                elif lastPathAdded == section:
                    continue
                # if section is not ".." then assume it is a valid bucket/folder
                else:

                    # need to check if the new cwlocn if at home, or in a bucket / folder
                    if newcwlocn == "" or newcwlocn == "/":
                        bucket = get_bucket_name("/" + section, "")
                        path = get_path("/" + section, "")
                    else:
                        bucket = get_bucket_name(newcwlocn, cwlocn)
                        path = get_path(section, newcwlocn)


                    all_buckets = bucket_list(s3)

                    # check if bucket exists
                    if bucket in all_buckets: 
                        
                        # if no folder/path to find, change cwlocn to bucket
                        if path == "":
                            dirLevel += 1
                            newcwlocn = "/" + bucket

                        # check if path ends with a suffix
                        # will have to be last path
                        elif pathlib.PurePath(path).suffix != "":
                            objects = object_list(s3_res, bucket)

                            if (path) in objects:
                                newcwlocn = "/" + bucket + "/" + path
                                dirLevel += 1

                                lastPathAdded = path
                            else:
                                print("file not found")
                                return cwlocn

                        # go through all folders
                        else:
                            objects = object_list(s3_res, bucket)

                            if (path + "/") in objects:
                                newcwlocn = "/" + bucket + "/" + path
                                dirLevel += 1

                                lastPathAdded = path
                            else:
                                print("folder not found")
                                return cwlocn

                    else:
                        print("bucket not found")
                        return cwlocn

        # if newcwlocn == "/":
        #     return ""
        
            return newcwlocn
        # return newcwlocn

    except:
        print("Cannot change directory")

#  
# List objects in bucket
# 

def list_objects(s3_res, bucketName):
    
    bucket = s3_res.Bucket(bucketName)

    for object in bucket.objects.all():
        print(object.key)

def object_list(s3_res, bucketName):
    bucket = s3_res.Bucket(bucketName)

    objects = []

    for object in bucket.objects.all():
        objects.append(str(object.key))

    return objects

#
#  List buckets
#

def list_long_buckets ( s3 ) :
    buckets = []
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        buckets.append("\t"+str(bucket["Name"]) +" | created: " + str(bucket['CreationDate']))

    for bucket in buckets:
        print ( bucket )
    ret = 0

    return ret

def list_buckets ( s3 ) :
    buckets = []
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        buckets.append("\t" + bucket["Name"])

    for bucket in buckets:
        print ( bucket )
    ret = 0

    return ret

def bucket_list ( s3 ) :
    buckets = []
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        buckets.append(bucket["Name"])
    return buckets

# 
# create bucket
# 

def bucket_create( s3, bname ):

    try:
        s3.create_bucket(Bucket=bname, CreateBucketConfiguration={'LocationConstraint': 'ca-central-1'})
        print ( "Current S3 Buckets" ) 
        ret = list_buckets ( s3 )
    except :
        print ( "Cannot create bucket ",bname )
        ret = 1

    return ret

# 
# copy local to cloud
# 

def local_to_s3_copy( s3 , localFile, bucketName, s3FilePath ):

    try:
        response = s3.upload_file(localFile, bucketName, s3FilePath)
        ret = 0
        print("Successfully copied [" + localFile + "] from local to S3 bucket [" + bucketName + "/" + s3FilePath+"]")
        return 0
    except:
        print("Unsuccessful copy")
        return 1

def locs3cp(s3, s3_res, localFile, s3Path, cwlocn):
    try:
        # this code will allow user to use ..
        if s3Path[0] == "/":
            parents = pathlib.PurePath(s3Path).parents
            s3_path = get_cwlocn(s3, s3_res, str(parents[0]), "/")
            s3FilePath = get_path(s3_path, "")

        else:
            parents = pathlib.PurePath(s3Path).parents
            s3_path = get_cwlocn(s3, s3_res, str(parents[0]), cwlocn)
            s3FilePath = get_path(s3_path, "")
        
        # will get the last section of path (the new object name)
        if(s3FilePath) == "":
            s3FilePath = pathlib.PurePath(s3Path).name
        else:
            s3FilePath += "/" + pathlib.PurePath(s3Path).name

        bucketName = get_bucket_name(s3_path, "")     

        # print("DEST: ", dest_path, dest_bucket, dest_key)

        # this code will not allow ..
        # bucketName = get_bucket_name(s3Path, cwlocn)
        # s3FilePath = get_path(s3Path, cwlocn)

        print(bucketName)
        print(s3FilePath)

        # print(s3FilePath)
        ret = local_to_s3_copy(s3,localFile, bucketName, s3FilePath)

        return ret
    except:
        ret = 1
        print("unable to copy from local to s3")
        return 0

# 
# copy cloud to local
# 

def s3_to_local_copy( s3 , localFile, bucketName, s3FilePath ):

    try:
        response = s3.download_file(bucketName, s3FilePath, localFile)
        print("Successfully copied [" + bucketName + "/" + s3FilePath+"] from S3 bucket to local [" + localFile +"]")
        return 0
    except:
        print("Unsuccessful copy")
        return 1

def s3loccp( s3 , s3_res, localFile , s3Path, cwlocn):
    try:

        if s3Path[0] == "/":
            parents = pathlib.PurePath(s3Path).parents
            s3_path = get_cwlocn(s3, s3_res, str(parents[0]), "/")
            s3FilePath = get_path(s3_path, "")

        else:
            parents = pathlib.PurePath(s3Path).parents
            s3_path = get_cwlocn(s3, s3_res, str(parents[0]), cwlocn)
            s3FilePath = get_path(s3_path, "")

        if(s3FilePath) == "":
            s3FilePath = pathlib.PurePath(s3Path).name
        else:
            s3FilePath += "/" + pathlib.PurePath(s3Path).name

        bucketName = get_bucket_name(s3_path, "")    

        # bucketName = get_bucket_name(s3Path, cwlocn)
        # s3FilePath = get_path(s3Path, cwlocn)

        ret = s3_to_local_copy(s3,localFile, bucketName, s3FilePath)
        return ret
    except:
        ret = 1
        print("unable to copy from s3 to local")
        return ret
    

# 
# create folder
# 

def folder_create( s3 , bname , folderPath ):

    try:
        sections = folderPath.split("/")
        # print(folderPath)
        base = ""
        for i in range(len(sections)):
            cur_section = sections[i]
            base += cur_section + "/"
            s3.put_object(Bucket=bname, Key=(base))

        # s3.put_object(Bucket=bname, Key=(folderPath + '/'))
        # print ( "Current S3 Buckets" ) 
        # ret = list_buckets ( s3 )
        ret = 0
        print( "Successfully created ["+folderPath+"] in bucket ["+bname+"]")
        return 0
    except :
        print ( "Cannot create folder 2", folderPath )
        return 1


# the folder path can be completely new and not part of s3
# assume they cant use ..
def create_folder ( s3 , s3_res, s3Path, cwlocn ):
    try:

        bname = get_bucket_name(s3Path, cwlocn)
        folderPath = get_path(s3Path, cwlocn)
        ret = folder_create(s3 , bname, folderPath)

        return ret
    except :
        print ( "Cannot create folder ", folderPath )
        return 1


# 
# change directory
# 

# this one can do only forward OR only backwards
def chlocn2 ( s3 , s3_res, s3Path , cwlocn):
    try:

        # this needs to be able to go back and forth between directories with .. and ../.. if you are currently in something
        # / or ~ can bring you back to "home"

        # if cwlocn == "/":]

        if s3Path == "/" or s3Path == "~":
            return ""

        # traverse through bucket and find folders
        bucket = get_bucket_name(s3Path, cwlocn)
        path = get_path(s3Path, cwlocn)

        all_buckets = bucket_list(s3)

        # check if bucket exists
        if bucket in all_buckets: 
            
            # if no folder/path to find, change cwlocn to bucket
            if path == "":
                print("changing location to specified bucket")
                return "/" + bucket

            else:
                print("finding folder in " + bucket)
                objects = object_list(s3_res, bucket)

                if (path + "/") in objects:
                    print("/" + bucket + "/" + path)
                    return "/" + bucket + "/" + path
                else:
                    print("folder not found")

        else:
            print("bucket not found")
    except:
        print("Cannot change directory")

def chlocn ( s3 , s3_res, s3Path , cwlocn):
    try:

        # this needs to be able to go back and forth between directories with .. and ../.. if you are currently in something
        # / or ~ can bring you back to "home"

        if s3Path == "/" or s3Path == "~":
            return "/"

        # split the inputted path
        pathSections = (s3Path).split("/")        

        if (pathSections[0] == ''):
            newcwlocn = s3Path
            bucket = get_bucket_name(s3Path, "")
            path = get_path(s3Path, "")

            all_buckets = bucket_list(s3)

            # check if bucket exists
            if bucket in all_buckets: 
                
                # if no folder/path to find, change cwlocn to bucket
                if path == "":
                    newcwlocn = "/" + bucket
                    return newcwlocn

                else:
                    objects = object_list(s3_res, bucket)

                    if (path + "/") in objects:
                        newcwlocn = "/" + bucket + "/" + path
                        return newcwlocn
                    else:
                        print("folder not found")
                        return cwlocn

            else:
                print("bucket not found")
                return cwlocn

        else: 

            # create a string that contains cwlocn (subject to change)
            newcwlocn = cwlocn
            dirLevel = len(newcwlocn.split("/"))
            lastPathAdded = ""

            # go through each section in inputted path
            for section in pathSections:
                # get the parents of cwlocn at begginning of for loop
                parents = pathlib.PurePath(newcwlocn).parents
                
                if dirLevel < 1: 
                    print("going back to home directory, went back too many times")
                    return "/"

                # if section has ".." then remove recent directory (with parents[0])
                if section == "..":
                    newcwlocn = str(parents[0])
                    dirLevel -= 1
                elif lastPathAdded == section:
                    continue
                # if section is not ".." then assume it is a valid bucket/folder
                else:

                    # need to check if the new cwlocn if at home, or in a bucket / folder
                    if newcwlocn == "" or newcwlocn == "/":
                        bucket = get_bucket_name("/" + section, "")
                        path = get_path("/" + section, "")
                    else:
                        bucket = get_bucket_name(newcwlocn, cwlocn)
                        path = get_path(section, newcwlocn)


                    all_buckets = bucket_list(s3)

                    # check if bucket exists
                    if bucket in all_buckets: 
                        
                        # if no folder/path to find, change cwlocn to bucket
                        if path == "":
                            dirLevel += 1
                            newcwlocn = "/" + bucket

                        else:
                            objects = object_list(s3_res, bucket)

                            if (path + "/") in objects:
                                newcwlocn = "/" + bucket + "/" + path
                                dirLevel += 1

                                lastPathAdded = path
                            else:
                                # print("folder not found")
                                return cwlocn

                    else:
                        # print("bucket not found")
                        return cwlocn

            # if newcwlocn == "/":
            #     return ""
        
            return newcwlocn

    except:
        print("Cannot change directory")

# 
# list function
# 
def s3List(s3, s3_res, s3Path, cwlocn, long):

    fullPath = get_full_path(s3, s3_res, s3Path, cwlocn)

    # check if fullPath is not "" or / then continue, if it is just / then list buckets
    # print(fullPath)

    ret = 0

    if fullPath == "/":
        print("Current S3 Buckets: ")
        if long == True:
            list_long_buckets(s3)
        else:
            list_buckets(s3)
        return 0
    else:

        bucket = get_bucket_name(fullPath, "/")
        path = get_path(fullPath, "/")

        # print(fullPath)

        # print(bucket)
        # print(path)

        all_buckets = bucket_list(s3)

        # check if bucket exists
        if bucket in all_buckets: 
            
            # if no folder/path to find, change cwlocn to bucket
            if path == "":
                # print("changing location to specified bucket")
                # list_objects(s3_res, bucket)
                response = s3.list_objects_v2(Bucket=bucket)
                fileCount = response['KeyCount']
                files = response.get("Contents")
                print("Contents of Bucket: ", bucket)
                
                if fileCount == 0:
                    print("Empty Bucket")
                else:
                    # print(len(list(files)))
                    for file in files:
                        if long == True:
                            print(f"\t| {file['Key']}\t size: {file['Size']}")
                        else:
                            print(f"\t| {file['Key']}")
            else:
                # print("finding folder in " + bucket)
                objects = object_list(s3_res, bucket)

                if (path + "/") in objects:
                    # print("FOUND FOLDER")
                    # print("path: ", path)
                    response = s3.list_objects_v2(Bucket=bucket, Prefix=path + "/")
                    fileCount = response['KeyCount']
                    files = response.get("Contents")
                    print("Contents of Bucket: ", bucket)
                    
                    if fileCount == 0:
                        print("Empty Bucket")
                    else:
                        for file in files:
                            if long == True:
                                print(f"\t| {file['Key']}, size: {file['Size']}")
                            else:
                                print(f"\t| {file['Key']}")
                    # print("/" + bucket + "/" + path)

                    # for object in bucket.objects.all():
                    #     print(object.key)
                    # return "/" + bucket + "/" + path
                    return 0
                else:
                    # print("folder not found")
                    ret = 1
        else:
            # print("couldnt find bucket")
            ret = 1
    
    return ret

# 
# copy s3 objects *
# 

def s3copy(s3, s3_res, s3source, s3dest, cwlocn):

    try: 

        source_bucket = get_bucket_name(s3source, cwlocn)
        source_key = get_path(s3source, cwlocn)

        if pathlib.PurePath(source_key).suffix == "":
            source_key += "/"

        dest_bucket = get_bucket_name(s3dest, cwlocn)
        dest_key = get_path(s3dest, cwlocn) 

        if pathlib.PurePath(dest_key).suffix == "":
            dest_key += "/"

        copy_source = {
            'Bucket': source_bucket,
            'Key': source_key
            }
        bucket = s3_res.Bucket(dest_bucket)
        bucket.copy(copy_source, dest_key)

        return 0
    except:
        print("error copying")
        return 1
    
# 
# delete objects
# 

def s3delete (s3, s3_res, s3Path, cwlocn):

    try:
    
        fullPath = get_full_path(s3, s3_res, s3Path, cwlocn)

        bucket = get_bucket_name(fullPath, "")
        key = get_path(fullPath, "")

        # bucket = get_bucket_name(s3Path, cwlocn)
        # key = get_path(s3Path, cwlocn)

        # need to check if path ends in "" or not


        if pathlib.PurePath(s3Path).suffix != "":
            # print("deleting file")
            object = s3_res.Object(bucket, key)
            object.delete()

        else:
            # print("checking folder for objects")

            # print(bucket)
            # print(key)

            cur_bucket = s3_res.Bucket(bucket)
            count = cur_bucket.objects.filter(Prefix=key+"/")
            
            object_count = len(list(count))
            # print(object_count)

            # only the folder exists, no other files
            if object_count == 1:
                # print("deleting folder")
                object = s3_res.Object(bucket, key)
                object.delete()
            else:
                print("error, cannot delete object")
                return 1
            
            
        return 0
    
    except:
        print("unable to delete s3 object")
        return 1

# 
# delete bucket
# 

def delete_bucket(s3 , bname):
    try:
        print("deleting bucket...")        

        objects = s3.list_objects_v2(Bucket=bname)
        fileCount = objects['KeyCount']

        if fileCount == 0:
            response = s3.delete_bucket(Bucket=bname)
            print("{} has been deleted successfully !!!".format(bname))
        else:
            print("{} is not empty, {} objects present".format(bname,fileCount))
            print("S3 bucket must be empty before deleting it")
            return 1
        
        return 0

    except:
        print("unable to delete bucket")
        return 1
