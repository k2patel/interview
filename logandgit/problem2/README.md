REST API: retrieve paginated data
=================================

GitHub exposes a lot of useful information about public repositories via its API. You can, for example, [retrieve a list of all public repositories belonging to an organization][1]. If there are many repositories, the reply is paginated.

[1]: https://docs.github.com/en/free-pro-team@latest/rest/reference/repos#list-organization-repositories

Your task in this problem is to retrieve a list of all public repositories in the `mozilla` and `mozilla-services` orgs, and then count how many of the repository names contain the substrings given in the input. Each input line contains a single string. On each output line, write that string and the number of repository names containing the string, separated by a space.

Since GitHub has severe rate limits for anonymous access, and the data on GitHub can change at any time, you should not use GitHub directly, but rather our simple API server with a static copy of the data located at https://hiring.cloudops.mozgcp.net/api/. We only support the `repos` endpoint described above, and only the query parameters that are relevant for pagination.
