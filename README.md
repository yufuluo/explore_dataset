1. Install dependancies
```
pip3 install -r requirements.txt
```

2. Convert CSV file to a table in SQLite (Optional. The table is already created so you can skip this step.)
```
python3 init_db.py

```
3. Run the server in port 5000
```
source env_var.sh
flask run -p 5000
```
4. The app is now running on `http://localhost:5000/`
