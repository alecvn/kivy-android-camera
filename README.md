# H1 Setup:

	virtualenv -p python3 --no-site-packages venv
	. venv/bin/activate
	pip install -r requirements.txt


# H1 Deploy to device:
	
	buildozer android debug deploy run logcat
