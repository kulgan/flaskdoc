[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2dafebf021354a42aa62b11d6ab42654)](https://www.codacy.com/manual/kulgan/flaskdoc?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kulgan/flaskdoc&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/2dafebf021354a42aa62b11d6ab42654)](https://www.codacy.com/manual/kulgan/flaskdoc?utm_source=github.com&utm_medium=referral&utm_content=kulgan/flaskdoc&utm_campaign=Badge_Coverage)
[![Build Status](https://travis-ci.com/kulgan/flaskdoc.svg?branch=master)](https://travis-ci.com/kulgan/flaskdoc)

# Flaskdoc
FlaskDoc is an extension of the regular Flask API and adds support for Swagger/OpenAPI documentation. 

## Requirements

* Python 2.7+, 3.5+

## Installation
Project is still in active development. The goal is to be able to install it like this
```bash
$ pip install flaskdoc
```

## Usage Examples
```python
import swagger.models
import flaskdoc
from flaskdoc import swagger

blp = flaskdoc.Blueprint("sample", __name__)

@blp.route("/echo/<string:sample>", 
    description="Simple Echo", 
    methods=[
        swagger.GET(tags=["sample"])
    ]
)
def echo(sample):
    return sample
```

## Release History

## Meta
Distributed under Apache 2.0 License

## Contributing
* Fork it
