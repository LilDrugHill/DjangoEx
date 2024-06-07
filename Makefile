start:
	python	sitewomen/manage.py	runserver

migrate:
	python	sitewomen/manage.py makemigrations

shell:
	python	sitewomen/manage.py	shell_plus	--print-sql
