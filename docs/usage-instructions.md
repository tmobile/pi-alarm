---
title: "Pi-Alarm Usage"
draft: false
---

There are two main ways to use your Pi-Alarm: The web interface and the REST API.

The web interface gives you a simple way of turning your alarm on or off over your network, or even the internet. The REST API is used for automation: You can use it to turn the alarm on or off in response to an event, such as a failure in a build pipeline. You can turn virtually anything into a switch using tools like [IFTTT](https://ifttt.com/), so get creative and share what you've made!

## Security

The `key_file.txt` defines users and their associated `key_access` code.  If there are entries in this file, access_key must be provided in the JSON request to turn the alarm on/off.  If there are no entries or all the entries are commented out, anyone can turn the alarm on/off.

## Logging

Logging configuration is defined in logging.conf.yaml.  By default, it will log both to console and to file (alarm.log)

## The Pi-Alarm REST API

{{< swagger file="alarm.swagger.yml" >}}

### End-Points

* /alarm/on
* /alarm/off