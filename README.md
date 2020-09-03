# weblate
# python scripts for creating weblate projects and components
1.If you want to create a project use the script ”autocreateprojects.py” we can use itwith 2 ways:
* This way for create a single project depend on the name.
  * python3 autocreateprojects.py 
  * --name=project-name
  * --web=company-url for the project
  * --host=host-url/api/projects
  * --auth= we can find it in ”https://weblate.test/accounts/profile/#api”
* This way for auto create the projects based on the bath.
  * python3 autocreateprojects.py
  * --path=path/to/projects/dir
  * --host–auth4.
* To create a components we can use autocreatecomponents.py script and we can useit by 2 ways as well.
  * This way for create a single component based on the name.
  * python3 autocreatecomponents.py
  * --name= component name
  * --repo= repo that you want to contribute with.
  * --branch= Repository branch to fetch translate.
  * --pushbranch= Repository branch to push translate the default branch is ”weblate_translation”
  * --host= host link.
  * --auth= please enter Authorization:Token token.
* This way for auto create components based on modules path.
  * python3 autocreatecomponents.py
  * --path= components path. 
  * --repo= repo that you want to contribute with.
  * --branch= Repository branch to fetch translate
  * --pushbranch= Repository branch to push translate the default branch is ”weblate_translation”.
  * --host= host link.
  * --auth= please enter Authorization:Token token5.
* Another script for exporting po files to the modules in a specific project path.
  * python3 exporttgz.py
  * --pathtoodoobin=path/to/odoo-bin.
  * --pathtomodules=path to project modules.
  * --d=database name
  * --l=language code
  * --v=python version 2 or 3.
