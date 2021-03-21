**Fast Json Normalize**

A package designed to be a drop in replacement for the pandas json normalize function, as it can be rather slow when dealing with very large json files.

It can be installed using

```
pip install fast-json-normalize
```

~(plan on making a pull request once I've integrated it into a fork of [Pandas](https://github.com/pandas-dev/pandas)~  

Pull request has been accepted into [Pandas](https://github.com/pandas-dev/pandas), see [40035](https://github.com/pandas-dev/pandas/pull/40035)  

Even with this been pulled into Pandas, this implementation should still be 50-80% faster, due to the Cython implementation, while the pull request I made with Pandas was pure Python

