# ADS Back-end task

Web service which receives a single string (bibliographic reference) and returns a JSON response containing the original string and the ADS identifier associated with the reference.

For example, for an input parameter like:

```
Abt, H. 1990, ApJ, 357, 1
```

The service will compute and return the expected identifier along with the original input string:


```JSON
{
   "refstring": "Abt, H. 1990, ApJ, 357, 1",
   "bibcode": "1990ApJ...357....1A"
}
```

## Requirements

To be able to run/test the application, an ADS API token is needed. It can be obtain following these instructions:

1. Create an account and log in to the latest version of the [ADS](https://ui.adsabs.harvard.edu/)
2. Push the "Generate a new key" button under Account - Customize settings - API Token

Then the key should be provided to the docker container or defined in the environment system like:

```bash
export ADS_DEV_KEY=K4aaZR79FowCVkPUxwMeYGnHEx5mVFJuwPvI5OYK 
```

If you want to run the application directly in your system (i.e., not using a docker container), then you need to make sure you have all the required python packages installed:

```bash
sudo pip install -r Service/requirements.txt
```

## Docker container

The service includes a docker description file to build a container which will run the service.

### Build container image

```bash
docker build -t marblestation/adsbackendtask .
```

### Run container

Run using the web service as it was copied when the image was built (replace the ADS token by your own one):

```bash
docker run -it --rm -p 127.0.0.1:5000:5000 -e ADS_DEV_KEY=K4aaZR79FowCVkPUxwMeYGnHEx5mVFJuwPvI5OYK marblestation/adsbackendtask
```

Run using the current local web service (useful for development purposes):

```bash
docker run -it --rm -p 127.0.0.1:5000:5000 -e ADS_DEV_KEY=K4aaZR79FowCVkPUxwMeYGnHEx5mVFJuwPvI5OYK -v ${PWD}/Service:/app marblestation/adsbackendtask
```

## Direct execution

If you do not want to use docker but just run the service in your system, you can launch it by executing (replace the ADS token by your own one):

```bash
cd Service/
python app.py
```

## Accessing the service

The application includes a simple HTML page that uses jQuery to call the REST service and resolve the refstrings indicated by the user, you can access it via [http://localhost:5000/](http://localhost:5000/). But you can also interact directly with the REST service using your browser and adding the refstring to the end of the URL: [http://localhost:5000/resolve/](http://localhost:5000/resolve/Abt,%20H.%201990,%20ApJ,%20357,%201)

It is also very easy to use the REST web service in an automatic way from a script. For instance, a python example:

```python
import requests
import urllib
refstring = "Abt, H. 1990, ApJ, 357, 1"
r = requests.get('http://localhost:5000/resolve/'+urllib.quote(refstring.replace("/", ":")))
response = r.json()
print(response['bibcode'])
print(response['status'])
```


## Tests

The application includes unit tests and a special separated test that processes a big number of refstrings (only thought to verify the efficiency of the resolver, not for frequent testing).

### Unit tests

The unit tests can be run by executing:

```bash
cd Service/
python test.py
```

The output will be directly printed on the screen, but if we want to save our results to a file we can do so by executing:

```bash
cd Service/
python test.py --log-filename ReferenceResolver/Tests/output/unit_tests_log.txt
```

### Sample of reference strings and bibcodes

The task included a file with an extensive list of bibcodes and refstrings, this test goes through all of them and saves the suggested bibcodes by the application:

```bash
python test_sample_process.py ReferenceResolver/Tests/input/refsample.txt ReferenceResolver/Tests/output/refsample_analysed.txt
```

Once the whole sample has been analysed, the results can be checked by executing:

```bash
python test_sample_report.py ReferenceResolver/Tests/output/refsample_analysed.txt ReferenceResolver/Tests/output/refsample_analysed_scores_hist.pdf ReferenceResolver/Tests/output/refsample_analysed_scores_hist.png
```

This will print some statistics using the python logging system, and it will create a histogram of the obtained scores comparing the total with the bibcodes that actually match the expected result (from the original sample file).

![Score histogram](Service/ReferenceResolver/Tests/output/refsample_analysed_scores_hist.png?raw=true)

