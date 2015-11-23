# CronMon

## Usage

```
your-task.sh arguments | cronmon --name your-task --location ~/cronmon
cronman --command "your-task.sh arguments" --name your-task --location ~/cronmon
cronmon --command "script.sh" --location ~/cronmon --on-fail "fail-script.sh"
```

## TODO

* ~~Store how much time does a task has taken~~
* ~~On failure do~~
* Configuration file
* Log into a single file
* Log into a database (SQL)
* Web server

## New CLI

```
cronmon run ...
cronmon log -n anaconda [0]
cronmon server
```

## Authors

`cronmon` was written by [Marcos Vanetta](http://twitter.com/malev).
