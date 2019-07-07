#!/bin/bash
echo "Start file copy"
cp /home/vsts/work/1/s/settings.py /home/vsts/work/1/s/propalyzer_site/propalyzer_site/
cp /home/vsts/work/1/s/secret.py /home/vsts/work/1/s/propalyzer_site/propalyzer_app/
cp /home/vsts/work/1/s/wsgi.py /home/vsts/work/1/s/propalyzer_site/propalyzer_site/
cp /home/vsts/work/1/s/urls.py /home/vsts/work/1/s/propalyzer_site/propalyzer_app/
echo "site dir below"
ls /home/vsts/work/1/s/propalyzer_site/propalyzer_site/
echo "app dir below"
ls /home/vsts/work/1/s/propalyzer_site/propalyzer_app/
echo "done!"
