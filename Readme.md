# S3 Storage Shell (S5)

**may need to install requirements.txt if not working
enter 'help' once within the shell to view all available S3 commands 

How to run the shell:
 - must have an S5-S3.conf set up for an AWS user
 - this configuration file must contain a [default] user with aws_access_key_id and aws_secret_access_key
 - S5-S3.conf must be in the same directory as s3shell.py
 - to run the shell, enter in terminal "python3 s3shell.py" 
 - from here you can enjoy all the benefits of being within your local and s3 shell

Normal Behaviour:
 - all functions act as displayed in the examples given in the assignment description
 - use '/' at the beginning of a path to indicate a bucket being accessed
 - a relative path will never start with a '/'
 - can use '..' for all functions except create_folder and s3copy

Limitations:
 - when doing list, if entering an invalid path it will output all the current buckets to show the user where they can be
 - cannot use '..' for create_folder and s3copy
