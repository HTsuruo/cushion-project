# cushion-project
admin page for cushion project.  

## Env.
* python 3.6.0
* Flask
* uWSGI
* Jinja2
* Flask-SQLAlchemy
* MySQL

## Run.
* install python libraries and static libraries.
```
pip install -r requirement.txt
bower install
```

* prodoction env.
```
uwsgi --ini uwsgi.ini
```

* development env. (port: 5000)
```
uwsgi --ini uwsgi_dev.ini
```

## Libraries.
* pip
	* requirement.txtに記載
* static file(css, js)
	* static/bower.jsonに記載

## Folders.
* ```app.py```
	* 実行ファイル
* ```/static```
	* css, jsなどの静的ファイル
* ```/templates```
	* htmlファイル
* ```calc.py```
	* グラフの生成や集中度計算などの計算処理全般が記述されている.
* ```util.py```
	* utility file
* ```uwsgi.ini```
	* 本番環境のuwsgi設定ファイル
* ```uwsgi_dev.ini```
	* 開発環境のuwsgi設定ファイル(ポートは5000番)
