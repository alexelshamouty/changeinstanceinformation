# changeinstanceinformation
Manipulating nova's instance information in the DB after properties change in the flavor


In my infrastructure we are saperating infrastructure based on certain criteria
At some point we wanted to change this criteria. The flavor is easy to change.
But the instance information can not be changed through the CLi. This scripts handles the needed changes in both the request_specs table and the instance_extras flavor.

No idea why nova is saving the information in two different places


TODO: Add a dry run
