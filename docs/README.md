---
title: "Raspberry Pi Alarm"
draft: false
---

# Pi-Alarm User Guide

This guide will take you step-by-step through building your own Pi-Alarm to control an alarm (or anything, really) with a Raspberry Pi over the internet! Development teams at [T-Mobile](https://opensource.t-mobile.com/) use Pi-Alarm to provide a clear visual alert to developers whenever something goes wrong in our build pipeline.

## Overall Design

**Before you get started**, it is important to understand the overall design of the Pi-Alarm.

The Raspberry Pi will run a Python program that acts as a simple web server to control a relay which is used to control the flow of electricity to the alarm (like an on/off switch). The program interacts with the relay through the Pi's GPIO pins via jumper wires. The relay switch is connected to an extension cord which powers the alarm.

![Design](images/design.jpg)

When assembing and testing the hardware, be sure to **follow all proper safety precautions**.

## Getting Started

To get up-and-running with a Pi-Alarm, there are two major steps:

1. [Install and Run the Pi-Alarm Software](software-instructions.md)
1. [Build the Pi-Alarm](build-instructions.md)

Once you've installed the Pi-Alarm software and connected all the hardware, you're ready to begin using your Pi-Alarm!

## Using Your Pi Alarm

Read the [usage instructions](usage-instructions.md) to begin using your Pi Alarm.

## Forking

We welcome people experimenting with different platforms and different software versions.  Please note that we cannot provide support or modifications for platforms and software different than what we use.  However, you should feel free to fork the tree for new platforms and software.  As per best practices, have your Information Technology department review this source code or any forks prior to any production or consequential use.  Please note that any forms of the tree are to comply with any open source licenses including Apache 2.0.