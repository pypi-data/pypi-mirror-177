# ExcelExtractor

ExcelExtractor handles maschine readable data for excel documents

ExcelExtrator handles excel worksheet with an headline and data under it.
It can read/write from those data and presents them in an maschine readable format in python
Needed file Structure in Excel:

```
|    A    |    B    |    C    | ....
+---------+---------+---------+-------
| ... 
+---------+---------+---------+-------
| Header1 | Header2 | Header3 | ...
+---------+---------+---------+-------
| Content | Content | Content | ...
+---------+---------+---------+-------
| ...
```

## Requirements

- Python >= 3.6
- openpyxl

## Installation

Install with pip

````
pip install excelextractor
````

## Documentation

https://dcfsec.github.io/excelextractor/

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/dcfSec/SecurityRatConnector/tags). 

## Authors

* [dcfSec](https://github.com/dcfSec) - *Initial work*

See also the list of [contributors](https://github.com/dcfSec/SecurityRatConnector/contributors) who participated in this project.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details

## ToDo

* Tests
* Documentation
