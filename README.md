(assumes you have Docker installed)

To containerise the API service:

```docker build -t fast-api .```
```docker run -d --name fast-api-app -p 80:80 fast-api```
