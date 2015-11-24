# CronMon

CronMon helps you monitor your cron tasks. Helps you handle the logging
and provides you a callback to know when something is wrong. It also
has a small webserver to help you navigate your logs.

## Usage

```
$ cronmon --help
Usage: cronmon [OPTIONS] COMMAND [ARGS]...

  CronMon helps you monitor your cron tasks. Helps you handle the logging
  and provides you a callback to know when something is wrong. It also has a
  small webserver to help you navigate your logs.

  Examples:

      cronmon -c your-script.sh
      cronmon -c your-script.sh -n your-project -f fail-script.sh
      cronmon --config config.yml

Options:
  --help  Show this message and exit.

Commands:
  log
  run
  server
```

Sample of a configuration file:

``` yml
name: cronmon
command: ls
location: /Users/malev/tmp
on_fail: ls
one_line: true
```

Note: the `one_line` option allows you to log everything in a single file.

## TODO

* ~~Store how much time does a task has taken~~
* ~~On failure do~~
* ~~Configuration file~~
* ~~Log into a single file~~
* Log into a database (SQL)
* Web server

## Authors

`cronmon` was written by [Marcos Vanetta](http://twitter.com/malev).
