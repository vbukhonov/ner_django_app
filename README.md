#Simple NER application built on Django.

This is a simple application which works on [Django](https://www.djangoproject.com/) 
engine for providing access via REST API. The technical information 
is stored in default [sqlite3](https://www.sqlite.org/index.html) DB.

The app is using [spaCy](https://spacy.io/) for running Named Entity Recognition
(NER) and [MongoDB](https://www.mongodb.com/) as a storage for the results.

### Installation and prerequisites
1. Clone repository.
2. Move to the project's folder and run `pip install -r requirements.txt`.
3. Set environment variable `DJANGO_SETTINGS_MODULE=ner_django_app.settings`.
    
    Note: migrations are not required here since we are not using Django models.

4. If you have some custom installation of MongoDB, set environment variables
`MONGO_DB_NAME` and `MONGO_DB_URI`.
5. Make sure that MongoDB server is running.
6. Optional: you can set `DEBUG=True`.

### Usage
1. Go to the project folder.
2. Put the input archives with patents as XML files to the folder `./inputs`.
    
    Note: such way of input was selected since the original requirement was
    to have ability to process ~10.000 files which is usually more convenient
    when files are stored in some SFTP or another folder-like storage.
    
3. Start the Django development server with command:
    ```
    ./ner_django_app/manage.py runserver 8000
    ```
4. Go to the [localhost:8000](http://127.0.0.1:8000/) (you will be
 automatically redirected to the required page.).
5. Press button `Run Pipeline` to process all archives in the `./inputs` folder.
6. You will see message "Success!" if everything is fine or "Something went
 wrong" if there was a failure.
7. Check the MongoDB where the results are stored in collection **patents**
 of DB `MONGO_DB_NAME`.
8. You can drop this collection by pressing button `Clean MongoDB`.

### Future TODOs
This application runs just general NER, without searching for any chemistry
 terms. We can use more specific library, e.g.
 [ChemDataExtractor](http://chemdataextractor.org/docs/gettingstarted).
