# ADS Back-end task

Web service which receives a single string (bibliographic reference) and returns a json response containing the original string and the ADS identifier associated with the reference.

For example, for an input parameter like:

```
Abt, H. 1990, ApJ, 357, 1
```

The service will compute and return the expected identifier along with the original input string:


```json
{
   "refstring": "Abt, H. 1990, ApJ, 357, 1",
   "bibcode": "1990ApJ...357....1A"
}
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

In both cases, you can access the service with your browser: http://localhost:5000/resolve/Abt,%20H.%201990,%20ApJ,%20357,%201


## Running and testing

If you do not want to use docker but just run the service in your system, you can launch it by executing (replace the ADS token by your own one):

```bash
cd Service/
ADS_DEV_KEY=K4aaZR79FowCVkPUxwMeYGnHEx5mVFJuwPvI5OYK python app.py
```

And you can access the service with your browser: http://localhost:5000/resolve/Abt,%20H.%201990,%20ApJ,%20357,%201

Or if you want to launch the automatic tests, you can execute:

```bash
cd Service/
ADS_DEV_KEY=K4aaZR79FowCVkPUxwMeYGnHEx5mVFJuwPvI5OYK python test.py
```

## How to get an ADS API token

1. Create an account and log in to the latest version of the [ADS](https://ui.adsabs.harvard.edu/)
2. Push the "Generate a new key" button under Account - Customize settings - API Token

