Beershift Server in Python on OpenShift Express
===============================================

This git repository helps you get up and running quickly with
a Beershift Server in Python
on OpenShift Express.


Running on OpenShift
----------------------------

Create an account at http://openshift.redhat.com/

Create a python-2.6 application

    rhc app create -a beershift -t python-2.6

Add this upstream beershift repo

    cd beershift
    git remote add upstream -m master git://github.com/openshift/beershift-python-demo.git
    git pull -s recursive -X theirs upstream master
    
Then push the repo upstream

    git push

That's it, you can now checkout your application at:

    http://beershift-$yournamespace.rhcloud.com

