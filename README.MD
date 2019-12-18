# Instructions for letsEncrypt
1. clone docker-images from github
2. edit buildtools/letsencrypt/request.ps1
    1. update line -d *.yourtld
    2. remove --dry-run if you are confident
3. run request.ps1
    1. Email: your email address
    2. Agree: yes
    3. Share Email: no
    4. IP logging: yes
4. azure portal DNS zone
    1. add _acme-challenge.* TXT record (e.g. _acme-challenge.vt) with the value provided from request.ps1
5. enter in request.ps1, it should run to completion
6. goto c:/letsencrypt/{DATE}/etc/archive/{url} (e.g. C:\letsencrypt\2019-11-08\etc\archive\testing.com )
7. copy contents of folder ( *.pem ) to your top level umbrella repo in the top level umbrella folder on the correct fork
8. check the changes in


