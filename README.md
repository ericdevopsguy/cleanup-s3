# cleanup-s3
Code from a coding challange. 

### Requirements: 

- Write a script that removes all but the most recent X deployments from an s3 bucket, where X is passed as a parameter.
- If a deployment is older than X, delete the entire folder.

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
