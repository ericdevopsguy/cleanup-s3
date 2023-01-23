# cleanup-s3
Code from a coding challange. 

### Requirements: 

- Write a script that removes all but the most recent X deployments from an s3 bucket, where X is passed as a parameter.
- If a deployment is older than X, delete the entire folder.

### Assumptions:

- That an s3 bucket exists named ```test-bucket``` and the user running the script has the necessary permissions (GetObject*, DeleteObject*, and ListBucket*).
- That the s3 object's last modified time is a reliable indicator of the deployment's age.
- That the script is run from a machine with the appropriate IAM credentials configured.. 

### Questions from Requirements:

- Where should we run this script? _This script should be run on a machine  with the appropriate IAM credentials (via profile or role) like so:_

```
    python3 cleanup-s3.py <number of deployments to keep as integer>
```
- How should we test the script before running it production? _Since this is a destructive operation, a "test" bucket should be used where it's okay to delete everything in the bucket._
- If we want to add an additional requirement of deleting deploys older than 30 days while keeping X deployments, what additional changes would you need to make in the script? _The current logic lists the "folders" in descending order, then keeps the most recent $X folders and deletes the rest. For it to meet these additional requirements, we could build a list of deployments, including their LastModified date/time. Using the current date, subtract 30 days to get the "delete after" date, then loop through the deployments. If the LastModified date is older than the "delete after" date, delete it. Care should be taken to ensure none of the "deployments to keep" are deleted. If one or more of the "deployments to keep" are older than 30 days, we could exit with a message stating the reason, or prompt the user to see if they still want to proceed with an "Are you sure?" type prompt. ***I would recommend just exiting the script with an error message to prevent an accidental “Y” from deleting production data.***_

### Opportunities for Refactoring:

- Add better error handling.
- Add logging, preferably to a centralized logging location.
- Use ```argparse``` for passing command line arguments.
- Break down some of these tasks into discrete functions (like filtering out "folder" keys).
- Add unit tests using pytest or similar.
- Add user prompts like _"The following objects will be deleted, are you sure?"_ then waiting for Y/n before proceeding.
- Add code and packaging so we can run it as a Lambda Function.
- Add a parameter for the s3 bucket name so it can be passed as an argument.

### Notes
The bucket I used for testing is configured like so:
```
    deployment-0/
        index.html
        style.css
    deployment-1/
        index.html
        style.css
    deployment-2/
        index.html
        style.css
    deployment-3/
        index.html
        style.css
    (and so on...)
```

Thanks! I really enjoyed this exercise. 

-Eric
