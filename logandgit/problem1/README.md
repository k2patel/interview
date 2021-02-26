Logs Analysis: Most frequent requests per hour
==============================================

We would like to investigate how the most frequent reuests to our web service change over the course of a day. To this end, we extract the most fequent request for each one-hour period from the web server logs.

The input to this problem is roughly a day's worth of nginx logs for a service that sits behind a CDN. The nginx configuration uses this format specification:

    log_format elb_dockerflow
        '$msec "$http_x_forwarded_for" "$request" $status $body_bytes_sent '
        '"$http_referer" "$http_user_agent" $request_time $upstream_response_time '
        '"$gzip_ratio" $upstream_cache_status';

For this problem we only need the first column, a floating-point number representing the Unix timestamp of the log entry, and the request string.

Requests are considered equal when the request method and request string as given in the logs are equal. There is no need to normalize the request strings in any way.

The one-hour windows should be aligned with full-hour boundaries. Since the log data starts and ends in the middle of an hour, there will be a total of 25 one-hour windows.

The output for each time window should be the ISO-8601-formatted UTC time (without any timezone desginator) of the beginning of the window, followed by the frequency of the most frequent request and the request string itself:

    2021-01-02T03:00:00 2 GET /v1/buckets/...

The most frequent request in each time window is unique.

You can look at the test cases in the `test_data` directory to see the full input and expected output.
