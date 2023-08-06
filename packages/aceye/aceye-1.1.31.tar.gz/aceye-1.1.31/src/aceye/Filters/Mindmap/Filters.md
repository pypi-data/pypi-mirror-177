
# Filters
## Name: est
### Name Alias: 
### Access Privilege: USER
### Annotation: 
### Apply To Fragments: no
### ARP OPC: unspecified
### Child Action: 
### Destination
#### From Port: unspecified
#### To Port: unspecified
### Description: 
### DN: uni/tn-common/flt-est/e-est
### EtherType: ip
### Externally Managed By: 
### ICMP
#### v4 T: unspecified
#### v6 T: unspecified
### Local Owner: local
### Match DSCP: unspecified
### Last Modified: 2022-11-17T15:49:20.367+00:00
### Monitoring Policy DN: uni/tn-common/monepg-default
### Protocol: tcp
### Source
#### From Port: unspecified
#### To Port: unspecified
### Stateful: no
### Status: 
### TCP Rules: est
### UID: 0
### User Domain: all
## Name: icmp
### Name Alias: 
### Access Privilege: USER
### Annotation: 
### Apply To Fragments: no
### ARP OPC: unspecified
### Child Action: 
### Destination
#### From Port: unspecified
#### To Port: unspecified
### Description: 
### DN: uni/tn-common/flt-icmp/e-icmp
### EtherType: ip
### Externally Managed By: 
### ICMP
#### v4 T: unspecified
#### v6 T: unspecified
### Local Owner: local
### Match DSCP: unspecified
### Last Modified: 2022-11-17T15:49:20.367+00:00
### Monitoring Policy DN: uni/tn-common/monepg-default
### Protocol: icmp
### Source
#### From Port: unspecified
#### To Port: unspecified
### Stateful: no
### Status: 
### TCP Rules: 
### UID: 0
### User Domain: all
## Name: default
### Name Alias: 
### Access Privilege: USER
### Annotation: 
### Apply To Fragments: no
### ARP OPC: unspecified
### Child Action: 
### Destination
#### From Port: unspecified
#### To Port: unspecified
### Description: 
### DN: uni/tn-common/flt-default/e-default
### EtherType: unspecified
### Externally Managed By: 
### ICMP
#### v4 T: unspecified
#### v6 T: unspecified
### Local Owner: local
### Match DSCP: unspecified
### Last Modified: 2022-11-17T15:49:20.367+00:00
### Monitoring Policy DN: uni/tn-common/monepg-default
### Protocol: unspecified
### Source
#### From Port: unspecified
#### To Port: unspecified
### Stateful: no
### Status: 
### TCP Rules: 
### UID: 0
### User Domain: all
## Name: arp
### Name Alias: 
### Access Privilege: USER
### Annotation: 
### Apply To Fragments: no
### ARP OPC: unspecified
### Child Action: 
### Destination
#### From Port: unspecified
#### To Port: unspecified
### Description: 
### DN: uni/tn-common/flt-arp/e-arp
### EtherType: arp
### Externally Managed By: 
### ICMP
#### v4 T: unspecified
#### v6 T: unspecified
### Local Owner: local
### Match DSCP: unspecified
### Last Modified: 2022-11-17T15:49:20.367+00:00
### Monitoring Policy DN: uni/tn-common/monepg-default
### Protocol: unspecified
### Source
#### From Port: unspecified
#### To Port: unspecified
### Stateful: no
### Status: 
### TCP Rules: 
### UID: 0
### User Domain: all
## Name: permit_all
### Name Alias: 
### Access Privilege: USER
### Annotation: 
### Apply To Fragments: no
### ARP OPC: unspecified
### Child Action: 
### Destination
#### From Port: unspecified
#### To Port: unspecified
### Description: 
### DN: uni/tn-TEST_GK/flt-VERITAS_deny_all_Fltr/e-permit_all
### EtherType: unspecified
### Externally Managed By: 
### ICMP
#### v4 T: unspecified
#### v6 T: unspecified
### Local Owner: local
### Match DSCP: unspecified
### Last Modified: 2022-11-17T16:03:22.886+00:00
### Monitoring Policy DN: uni/tn-common/monepg-default
### Protocol: unspecified
### Source
#### From Port: unspecified
#### To Port: unspecified
### Stateful: no
### Status: 
### TCP Rules: 
### UID: 15374
### User Domain: :all:
## Name: permit_all
### Name Alias: 
### Access Privilege: USER
### Annotation: 
### Apply To Fragments: no
### ARP OPC: unspecified
### Child Action: 
### Destination
#### From Port: unspecified
#### To Port: unspecified
### Description: 
### DN: uni/tn-TEST_GK/flt-VERITAS_permit_all_Fltr/e-permit_all
### EtherType: unspecified
### Externally Managed By: 
### ICMP
#### v4 T: unspecified
#### v6 T: unspecified
### Local Owner: local
### Match DSCP: unspecified
### Last Modified: 2022-11-17T16:03:22.886+00:00
### Monitoring Policy DN: uni/tn-common/monepg-default
### Protocol: unspecified
### Source
#### From Port: unspecified
#### To Port: unspecified
### Stateful: no
### Status: 
### TCP Rules: 
### UID: 15374
### User Domain: :all:
## Name: tcp_9001-9002
### Name Alias: 
### Access Privilege: USER
### Annotation: 
### Apply To Fragments: no
### ARP OPC: unspecified
### Child Action: 
### Destination
#### From Port: 9001
#### To Port: 9002
### Description: 
### DN: uni/tn-common/flt-power_up/e-tcp_9001-9002
### EtherType: ip
### Externally Managed By: 
### ICMP
#### v4 T: unspecified
#### v6 T: unspecified
### Local Owner: local
### Match DSCP: unspecified
### Last Modified: 2022-11-17T18:22:49.369+00:00
### Monitoring Policy DN: uni/tn-common/monepg-default
### Protocol: tcp
### Source
#### From Port: unspecified
#### To Port: unspecified
### Stateful: no
### Status: 
### TCP Rules: 
### UID: 15374
### User Domain: :all:
## Name: tcp-1433
### Name Alias: 
### Access Privilege: USER
### Annotation: 
### Apply To Fragments: no
### ARP OPC: unspecified
### Child Action: 
### Destination
#### From Port: 1433
#### To Port: 1433
### Description: 
### DN: uni/tn-common/flt-sql_server/e-tcp-1433
### EtherType: ip
### Externally Managed By: 
### ICMP
#### v4 T: unspecified
#### v6 T: unspecified
### Local Owner: local
### Match DSCP: unspecified
### Last Modified: 2022-11-17T18:22:49.369+00:00
### Monitoring Policy DN: uni/tn-common/monepg-default
### Protocol: tcp
### Source
#### From Port: unspecified
#### To Port: unspecified
### Stateful: no
### Status: 
### TCP Rules: 
### UID: 15374
### User Domain: :all:
## Name: udp-1434
### Name Alias: 
### Access Privilege: USER
### Annotation: 
### Apply To Fragments: no
### ARP OPC: unspecified
### Child Action: 
### Destination
#### From Port: 1434
#### To Port: 1434
### Description: 
### DN: uni/tn-common/flt-sql_browser/e-udp-1434
### EtherType: ip
### Externally Managed By: 
### ICMP
#### v4 T: unspecified
#### v6 T: unspecified
### Local Owner: local
### Match DSCP: unspecified
### Last Modified: 2022-11-17T18:22:49.369+00:00
### Monitoring Policy DN: uni/tn-common/monepg-default
### Protocol: udp
### Source
#### From Port: unspecified
#### To Port: unspecified
### Stateful: no
### Status: 
### TCP Rules: 
### UID: 15374
### User Domain: :all:
## Name: tcp-80
### Name Alias: 
### Access Privilege: USER
### Annotation: 
### Apply To Fragments: no
### ARP OPC: unspecified
### Child Action: 
### Destination
#### From Port: http
#### To Port: http
### Description: 
### DN: uni/tn-common/flt-http/e-tcp-80
### EtherType: ip
### Externally Managed By: 
### ICMP
#### v4 T: unspecified
#### v6 T: unspecified
### Local Owner: local
### Match DSCP: unspecified
### Last Modified: 2022-11-17T18:22:49.369+00:00
### Monitoring Policy DN: uni/tn-common/monepg-default
### Protocol: tcp
### Source
#### From Port: unspecified
#### To Port: unspecified
### Stateful: no
### Status: 
### TCP Rules: 
### UID: 15374
### User Domain: :all:
## Name: tcp-443
### Name Alias: 
### Access Privilege: USER
### Annotation: 
### Apply To Fragments: no
### ARP OPC: unspecified
### Child Action: 
### Destination
#### From Port: https
#### To Port: https
### Description: 
### DN: uni/tn-common/flt-https/e-tcp-443
### EtherType: ip
### Externally Managed By: 
### ICMP
#### v4 T: unspecified
#### v6 T: unspecified
### Local Owner: local
### Match DSCP: unspecified
### Last Modified: 2022-11-17T18:22:49.369+00:00
### Monitoring Policy DN: uni/tn-common/monepg-default
### Protocol: tcp
### Source
#### From Port: unspecified
#### To Port: unspecified
### Stateful: no
### Status: 
### TCP Rules: 
### UID: 15374
### User Domain: :all:
## Name: tcp-80
### Name Alias: 
### Access Privilege: USER
### Annotation: 
### Apply To Fragments: no
### ARP OPC: unspecified
### Child Action: 
### Destination
#### From Port: http
#### To Port: http
### Description: 
### DN: uni/tn-SnV/flt-http/e-tcp-80
### EtherType: ip
### Externally Managed By: 
### ICMP
#### v4 T: unspecified
#### v6 T: unspecified
### Local Owner: local
### Match DSCP: unspecified
### Last Modified: 2022-11-17T18:22:50.147+00:00
### Monitoring Policy DN: uni/tn-common/monepg-default
### Protocol: tcp
### Source
#### From Port: unspecified
#### To Port: unspecified
### Stateful: no
### Status: 
### TCP Rules: 
### UID: 15374
### User Domain: :all:
## Name: tcp-1433
### Name Alias: 
### Access Privilege: USER
### Annotation: 
### Apply To Fragments: no
### ARP OPC: unspecified
### Child Action: 
### Destination
#### From Port: 1433
#### To Port: 1433
### Description: 
### DN: uni/tn-SnV/flt-sql/e-tcp-1433
### EtherType: ip
### Externally Managed By: 
### ICMP
#### v4 T: unspecified
#### v6 T: unspecified
### Local Owner: local
### Match DSCP: unspecified
### Last Modified: 2022-11-17T18:22:50.147+00:00
### Monitoring Policy DN: uni/tn-common/monepg-default
### Protocol: tcp
### Source
#### From Port: unspecified
#### To Port: unspecified
### Stateful: no
### Status: 
### TCP Rules: 
### UID: 15374
### User Domain: :all: