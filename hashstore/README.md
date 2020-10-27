## /messages

Accepts a JSON message as a POST. The message should adhere to the following format:

```

{

  “message”: “this is a sample message!”

}

```

The contents of the message should be a string.

 

The response should contain the SHA256 of the string content of the original message as a hexadecimal string. It should resemble the following:

```

{

   “digest” : “bdfcba37390f1dc3d871011777098dab32c8dd9542b56291268ed950c8b58ba7”

}

```




## /messages/<hash>

Accepts the SHA256 of a message as a GET parameter and returns the content of the original message as a string. A request to a non-existent SHA256 hash should return a 404 along with an error message.

 

A successful response should resemble the following:

 

```

{

  “message”: “this is a sample message!”

}

```

 

An unsuccessful response should respond with the following JSON:

```

{

  “error”: “unable to find message”,

“message_sha256”: “abc123” 

}

```

 

## /messages/<hash>

The /messages endpoint also accepts the SHA256 hash of a message with a DELETE method which will delete the message if it exists.

 

The API should return 200 OK if the message was deleted or if the message did not exist. It should return the appropriate error code if the API encounters a problem while attempting to delete the message.




## /metrics

Handle a GET request that retrieves runtime metrics from your service. The format and content is up to you, but you should include any measurements you would want to see when monitoring this service in production.





## Example

Let’s say you expose port 8080:

```shell

$ curl -X POST -H "Content-Type: application/json" -d '{"message": "foo"}'

http://localhost:8080/messages

{

   "digest": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"

}

```

 

You can calculate that your result is correct on the command line:

```shell

$ echo -n "foo" | shasum -a 256 2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae -

```

 

You can now query your service for the original message:

```shell

$ curl http://localhost:8080/messages/2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f9

8a5e886266e7ae

{

   "message": "foo"

}

$ curl -i http://localhost:8080/messages/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

aaaaaaaaaaaaaa HTTP/1.0 404 NOT FOUND Content-Type: application/json Content-Length: 36

Server: Werkzeug/0.11.5 Python/3.5.1 Date: Wed, 31 Aug 2016 14:21:11 GMT

{

   "error": "unable to find message",

   “message_sha256”: “aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

aaaaaaaaaaaaaa”

}

```

# Application Dockerfile

This repository contains **Dockerfile**.

## Base Docker Image

* [dockerfile/python:latest](https://github.com/docker-library/python)

## Installation

1. Install [Docker](https://www.docker.com/).

   (you can build an image from Dockerfile: `docker build -t="test_instanace" .`)

## Usage

    docker run -d -p 5000:5000 test_instanace:latest

### Attach persistent/shared directories

    docker run -d -p 5000:5000 -v ~/data:/usr/src/app/data test_instanace:latest

After few seconds, open `http://localhost:5000` to see the welcome page.

# Instanace / Application Metrics

## Metric types

The Prometheus client libraries offer four core metric types. These are
currently only differentiated in the client libraries (to enable APIs tailored
to the usage of the specific types) and in the wire protocol. The Prometheus
server does not yet make use of the type information and flattens all data into
untyped time series. This may change in the future.

## Counter

A _counter_ is a cumulative metric that represents a single [monotonically 
increasing counter](https://en.wikipedia.org/wiki/Monotonic_function) whose
value can only increase or be reset to zero on restart. For example, you can
use a counter to represent the number of requests served, tasks completed, or
errors.

Do not use a counter to expose a value that can decrease. For example, do not
use a counter for the number of currently running processes; instead use a gauge.

Client library usage documentation for counters:

   * [Python](https://github.com/prometheus/client_python#counter)

## Gauge

A _gauge_ is a metric that represents a single numerical value that can
arbitrarily go up and down.

Gauges are typically used for measured values like temperatures or current
memory usage, but also "counts" that can go up and down, like the number of
concurrent requests.

Client library usage documentation for gauges:

   * [Python](https://github.com/prometheus/client_python#gauge)

## Histogram

A _histogram_ samples observations (usually things like request durations or
response sizes) and counts them in configurable buckets. It also provides a sum
of all observed values.

A histogram with a base metric name of `<basename>` exposes multiple time series
during a scrape:

  * cumulative counters for the observation buckets, exposed as `<basename>_bucket{le="<upper inclusive bound>"}`
  * the **total sum** of all observed values, exposed as `<basename>_sum`
  * the **count** of events that have been observed, exposed as `<basename>_count` (identical to `<basename>_bucket{le="+Inf"}` above)

Use the
[`histogram_quantile()` function](/docs/prometheus/latest/querying/functions/#histogram_quantile)
to calculate quantiles from histograms or even aggregations of histograms. A
histogram is also suitable to calculate an
[Apdex score](http://en.wikipedia.org/wiki/Apdex). When operating on buckets,
remember that the histogram is
[cumulative](https://en.wikipedia.org/wiki/Histogram#Cumulative_histogram). See
[histograms and summaries](/docs/practices/histograms) for details of histogram
usage and differences to [summaries](#summary).

Client library usage documentation for histograms:

   * [Python](https://github.com/prometheus/client_python#histogram)

## Summary

Similar to a _histogram_, a _summary_ samples observations (usually things like
request durations and response sizes). While it also provides a total count of
observations and a sum of all observed values, it calculates configurable
quantiles over a sliding time window.

A summary with a base metric name of `<basename>` exposes multiple time series
during a scrape:

  * streaming **φ-quantiles** (0 ≤ φ ≤ 1) of observed events, exposed as `<basename>{quantile="<φ>"}`
  * the **total sum** of all observed values, exposed as `<basename>_sum`
  * the **count** of events that have been observed, exposed as `<basename>_count`

See [histograms and summaries](/docs/practices/histograms) for
detailed explanations of φ-quantiles, summary usage, and differences
to [histograms](#histogram).

Client library usage documentation for summaries:

   * [Python](https://github.com/prometheus/client_python#summary)