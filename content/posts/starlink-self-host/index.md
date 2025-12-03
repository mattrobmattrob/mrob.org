---
title: "Self hosting website on Starlink"
date: "2025-12-02"
lang: "en"
authors: ["Matt Robinson"]
categories: ["Software"]
tags: ["self-host"]
draft: true
---

Starlink claims to support native IPv6 across all equipment ([from the Help Center](https://starlink.com/support/article/1192f3ef-2a17-31d9-261a-a59d215629f4)):

>Starlink offers two IPv4 policies, "default" and "public". The default IPv4 configuration uses Carrier-Grade Network Address Translation (CGNAT) using private address space from the 100.64.0.0/10 prefix assigned to Starlink clients via DHCP. Network Address Translation (NAT) translates between private and Starlink public IPv4 Addresses. Starlink supports native IPv6 across all Starlink routers, kit versions, and service plans. All IPv6 compatible Starlink router clients are assigned IPv6 addresses.

But, they also do CGNAT (explained above), which requires the use of IPv6 to reference a specific network/router/computer on their broader network.

<!-- TALK ABOUT ASUS NETWORK IPv6 SETTINGS -->

Raspberry Pi running Debian needs to have IPv6 enabled (based on [this approach](https://reintech.io/blog/setting-up-ipv6-networking-debian-12)).

Do you currently have an IPv6 address?
```
ip addr show | grep inet6
```

Add the following to `/etc/sysctl.conf` (it might not exist):
```
net.ipv6.conf.all.disable_ipv6 = 0
net.ipv6.conf.default.disable_ipv6 = 0
```

Apply the changes:
```
sudo sysctl -p
```

Do you have an IPv6 address now?
```
$ ip addr show | grep inet6
inet6 ::1/128 scope host noprefixroute
inet6 2605:59c8:5200:6f91:ba27:ebff:fe86:c76a/64 scope global dynamic mngtmpaddr proto kernel_ra
inet6 fe80::ba27:ebff:fe86:c76a/64 scope link proto kernel_ll
```

It worked! Now, update the DNS AAAA record to `2605:59c8:5200:6f91:ba27:ebff:fe86:c76a` on your domain name registrar's site.
