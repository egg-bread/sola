# sola

sola is a simple JSON to CSV script/program for Otogi written in Python. 
<br/>It grabs daemon data from the input JSON file and writes it to a nicely formatted CSV file (with a header!) for easier data manipulation.

## Getting Started

You will need:
* [Python 3.6+](https://www.python.org/downloads/) 
* [sola.py](sola.py)
* input JSON file (or use echo.json in example folder)
* a working computer

Move sola.py and the JSON file into the **same directory**. This could be your Desktop or any other easily accessible location. **The output CSV file will be in the same directory as sola.py and the JSON file.**

## Running sola

When sola asks for any file name, enter it **without the extension**. 
<br/>For example, if the JSON file name is *filename.json*, enter it as *filename*:

```
Enter json file name: filename
```

### Using Bash

```
$ python3 sola.py
```

Example run where the JSON file name is *echo.json* and the file name I want to write to is *daemon-info.csv*:

```
$ python3 sola.py
Enter json file name: echo
Enter file name to write daemon information to: daemon-info
sola has finished writing to 'daemon-info.csv'
```

### Using cmd

```
placeholder
```

Example run:

```
placeholder
```

## Authors

* [tofubridge](https://github.com/tofubridge)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
Thanks to the people who *inspired* me to create sola :slightly_smiling_face: 
