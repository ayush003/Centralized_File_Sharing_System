# Centralized File Sharing System With Server-Client Architecture

Implemented Commands:

1. `IndexGet flag(args)`
  - Can request the display of the shared files on the connected system.
  - The history of requests made by either user is maintained at each user's system respectively.
  - The flag variable can be shortlist or longlist.
  - `Shortlist`:
    - Returns the names of files between a specific set of timestamps.
    The sample query is shown below:
    - $> `IndexGet shortlist <starttimestamp> <endtimestamp>`
    - Output includes ‘name’ , ‘size’ ,‘timestamp’ and ‘type’ of the files between the start and end time stamps.
    - Return only *.txt , *.pdf files between specified time stamps with this type of query:
      $> `IndexGet shortlist <starttimestamp> <endtimestamp> *.txt or *.pdf`
  - `Longlist` : 
    - Returns the entire listing of the shared directory including ‘name’, ‘size’, ‘timestamp’ and ‘type’ of the files.
    - `$>IndexGet longlist`
    - Output : similar to above , but with complete listing.
    - Return only *.txt , *.pdf files with this type of query:
          $> `IndexGet longlist *.txt or *.pdf`
          
2. `FileHash flag(args)` :
  - Check if any of the files on the other end have been changed. The flag variable can take two values, verify and checkall.
  - `Verify` :
    - Checks for the specific file name provided as command line argument and return its ‘checksum’ and ‘last modified’ timestamp.
    - `$>FileHash verify <filename>`
    - Output : checksum and lastmodified timestamp of the input file.
  - `Checkall` :
    - flag should check perform what ‘verify’ does for all the files in the shared folder.
    - `$> FileHash checkall`
    - Output : filename , checksum and last modified timestamp of all the files in the shared directory.
    
3. `FileDownload flag` :
  - Download files from the shared folder of connected user to our shared folder.
  - `$>FileDownload <filename>`
  - Output : filename , filesize ,lastmodified timestamp and the MD5hash of the requested file.

4. `Cache flag(args)` :
  - Check and update the contents of the Cache.
  - `$> Cache show`
      - Output : filename , filesize ,lastmodified timestamp and the MD5hash of all the files in the Cache Folder.
  - `$> Cache verify <filename>`
      - Verifies that the <filename> is already present in the cache. If not present, then the client downloads <filename> to the cache.
