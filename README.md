# CronMon

## Usage

```
cronman --command "your-task.sh arguments" --name your-task --location ~/cronmon
cronmon --command "script.sh" --location ~/cronmon --on-fail "fail-script.sh"
```

Or using a `config.yml` file:

``` yml
name: cronmon
command: ls
location: /Users/malev/tmp
on_fail: ls
```

```
cronmon --config config.yml
```

## TODO

* ~~Store how much time does a task has taken~~
* ~~On failure do~~
* ~~Configuration file~~
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
