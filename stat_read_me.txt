Stat Structure

This is the main readme file for the Google App Engine (GAE) based Stat with GAE Boilerplate and Twitter's Bootstrap.

Organization: the frame is MVC based. To quickly learn the structure follow the path: main.py >> routes.py >> handlers.py >> (models.py, forms.py ... and some settings are in the config files: /config/localhost.py)

Folder structure:
> boilerplate (sub-dirs) the skeleton that runs the site out of the box. Don't modify anything here. Use the structure here as an example only and override with elements in:
> static - the CSS, IMG, JS, etc
> templates - our html
> web - our Python code


Follow the trail:
Main.py >> routes.py

handlers.py: handles different parts of HTTP request and response, applies some business logic, and redirects to a page (.html) or a path in is routes.py


Build our own:
- modify routes.py in the root dir (entered two routes)
- modify main.py and add routes (from web import routes as stat_routes)
- modify handlers.py in web dir. Write code to handle data processing before sending params to .html or route
	- the most basic handler does: return self.render_template('contact.html', **params) 
- flow: basehandler.py (now in BP, need to move) >> base.html >> page.html (in templates)
- register a user locally: register on the home page. Go to admin: http://localhost:8081/admin/users. Edit user, activate. Go to home page. Login. You get a different view.

Forms:
- each form has a unique id: e.g., id="form_contact"
- the forms on the form (must / may) match what's in the forms.py file. NOTE: for now the forms.py file is located under the boilerplate. In the future all JoinHour forms should be pulled out out of boilerplate.
-  enter form's variables in the basehandler.py in the boilerplate.     
	e.g.,	@webapp2.cached_property
		 	   def activity_status(self):
		    	    return self.session.get_flashes(key='_activity_status')

Notes:
copied all files from the boilerplate/templates to /templates to correctly use the desired base.html
TODO: get rid of the /templates in the boilerplate/tempaltes folder?
TODO: update style.css to add the image back
