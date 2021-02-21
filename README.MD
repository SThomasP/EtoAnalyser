# Etymology Analyser

The eventual plan is to be able to generate a visualisation of the various etymologies of a block of English text, for now it's just a database generator.


## The database
The database of etymological relations is generated from 
[Gerard de Melo's](http://gerard.demelo.org/) dataset, which is based on the contributions of the [English Wiktionary community](
http://en.wiktionary.org/).

It can be generated using the following command line:
```
python3 -m database.builder 
```
Which will generate the database at database/data/etymologies.db.

The generated database is licensed under CC-BY-SA 3.0.

## License

The generated database is licensed under the CC-BY-SA 3.0. Anything else remains unlicensed, a license may be issued when the project is complete.