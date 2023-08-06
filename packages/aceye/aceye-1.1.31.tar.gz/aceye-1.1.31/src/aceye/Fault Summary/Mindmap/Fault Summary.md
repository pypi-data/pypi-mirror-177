
# Fault Summary
## Cause: protocol-arp-adjacency-down
### Child Action: 
### Code: F1207
### Count: 1
### Description: This fault occurs when the operational state of the arp adjacency is down
### DN: fltcode-F1207
### Domain: access
### Non
#### Acknowledged: 1
#### Delegated: 1
#### Delagated And Acknowledged: 1
### Rule: arp-st-adj-ep-oper-st-down
### Severity: warning
### Status: 
### Subject: oper-state-change
### Type: operational
## Cause: threshold-crossed
### Child Action: 
### Code: F110344
### Count: 22
### Description: Threshold crossing alert for class l2IngrBytesPart5min, property dropRate
### DN: fltcode-F110344
### Domain: infra
### Non
#### Acknowledged: 22
#### Delegated: 0
#### Delagated And Acknowledged: 0
### Rule: tca-l2-ingr-bytes-part5min-drop-rate
### Severity: warning
### Status: 
### Subject: counter
### Type: operational
## Cause: threshold-crossed
### Child Action: 
### Code: F112128
### Count: 28
### Description: Threshold crossing alert for class l2IngrPkts5min, property dropRate
### DN: fltcode-F112128
### Domain: infra
### Non
#### Acknowledged: 28
#### Delegated: 6
#### Delagated And Acknowledged: 6
### Rule: tca-l2-ingr-pkts5min-drop-rate
### Severity: warning
### Status: 
### Subject: counter
### Type: operational
## Cause: threshold-crossed
### Child Action: 
### Code: F110473
### Count: 4
### Description: Threshold crossing alert for class l2IngrBytesAg15min, property dropRate
### DN: fltcode-F110473
### Domain: infra
### Non
#### Acknowledged: 4
#### Delegated: 4
#### Delagated And Acknowledged: 4
### Rule: tca-l2-ingr-bytes-ag15min-drop-rate
### Severity: warning
### Status: 
### Subject: counter
### Type: operational
## Cause: threshold-crossed
### Child Action: 
### Code: F110176
### Count: 28
### Description: Threshold crossing alert for class l2IngrBytes5min, property dropRate
### DN: fltcode-F110176
### Domain: infra
### Non
#### Acknowledged: 28
#### Delegated: 6
#### Delagated And Acknowledged: 6
### Rule: tca-l2-ingr-bytes5min-drop-rate
### Severity: warning
### Status: 
### Subject: counter
### Type: operational
## Cause: dhcpd-fnv-out-of-sync
### Child Action: 
### Code: F4144
### Count: 1
### Description: This fault is raised when dhcp client and pool are not in sync with fnv data
### DN: fltcode-F4144
### Domain: infra
### Non
#### Acknowledged: 1
#### Delegated: 1
#### Delagated And Acknowledged: 1
### Rule: dhcp-discovery-health-dhcpd-fnv-un-sync
### Severity: major
### Status: 
### Subject: dhcp
### Type: operational
## Cause: configuration-failed
### Child Action: 
### Code: F1690
### Count: 7
### Description: This fault occurs when there is incomplete or incorrect configuration, intermittent system errors.
### DN: fltcode-F1690
### Domain: tenant
### Non
#### Acknowledged: 7
#### Delegated: 7
#### Delagated And Acknowledged: 7
### Rule: vns-conf-issue-conf-issue
### Severity: minor
### Status: 
### Subject: management
### Type: config
## Cause: threshold-crossed
### Child Action: 
### Code: F381328
### Count: 15
### Description: Threshold crossing alert for class eqptIngrErrPkts5min, property crcLast
### DN: fltcode-F381328
### Domain: infra
### Non
#### Acknowledged: 15
#### Delegated: 15
#### Delagated And Acknowledged: 15
### Rule: tca-eqpt-ingr-err-pkts5min-crc-last
### Severity: warning
### Status: 
### Subject: counter
### Type: operational
## Cause: configuration-failed
### Child Action: 
### Code: F0772
### Count: 1
### Description: This fault occurs when a Logical Interface configuration is invalid.The config issues the exact reason for the error.
### DN: fltcode-F0772
### Domain: tenant
### Non
#### Acknowledged: 1
#### Delegated: 1
#### Delagated And Acknowledged: 1
### Rule: vns-alif-validation-failed
### Severity: minor
### Status: 
### Subject: management
### Type: config
## Cause: equipment-psu-missing
### Child Action: 
### Code: F1318
### Count: 2
### Description: This fault occurs when PSU are not detected correctly
### DN: fltcode-F1318
### Domain: infra
### Non
#### Acknowledged: 2
#### Delegated: 2
#### Delagated And Acknowledged: 2
### Rule: eqpt-psg-pzero-pwr
### Severity: major
### Status: 
### Subject: power-group
### Type: environmental
## Cause: product-not-registered
### Child Action: 
### Code: F3057
### Count: 1
### Description: This fault is raised when APIC Controller product is not registered with Cisco Smart Software Manager (CSSM).
### DN: fltcode-F3057
### Domain: external
### Non
#### Acknowledged: 1
#### Delegated: 1
#### Delagated And Acknowledged: 1
### Rule: license-manager-product-not-registered
### Severity: warning
### Status: 
### Subject: smart-licensing
### Type: config
## Cause: dhcp-client-missing-lease
### Child Action: 
### Code: F4141
### Count: 1
### Description: This fault is raised when there is dhcp client without a lease
### DN: fltcode-F4141
### Domain: infra
### Non
#### Acknowledged: 1
#### Delegated: 1
#### Delagated And Acknowledged: 1
### Rule: dhcp-discovery-health-dhcp-client-lease-check-failed
### Severity: warning
### Status: 
### Subject: dhcp
### Type: operational
## Cause: config-error
### Child Action: 
### Code: F3083
### Count: 72
### Description: This fault occurs when multiple MACs have same IP address in the same VRF.
### DN: fltcode-F3083
### Domain: tenant
### Non
#### Acknowledged: 72
#### Delegated: 72
#### Delagated And Acknowledged: 72
### Rule: fv-ip-config-error
### Severity: major
### Status: 
### Subject: same-ip-address-is-used-by-different-macs-in-the-same-context
### Type: config
## Cause: protocol-coop-adjacency-down
### Child Action: 
### Code: F1360
### Count: 2
### Description: This fault occurs when the operational state of the coop adjacency is down
### DN: fltcode-F1360
### Domain: access
### Non
#### Acknowledged: 2
#### Delegated: 2
#### Delagated And Acknowledged: 2
### Rule: coop-adj-ep-coop-adj-ep-down
### Severity: warning
### Status: 
### Subject: oper-state-down
### Type: operational
## Cause: configuration-failed
### Child Action: 
### Code: F0467
### Count: 68
### Description: This fault occurs when an End Point Group / End Point Security Group is incompletely or incorrectly configured.
### DN: fltcode-F0467
### Domain: tenant
### Non
#### Acknowledged: 68
#### Delegated: 34
#### Delagated And Acknowledged: 34
### Rule: fv-nw-issues-config-failed
### Severity: minor
### Status: 
### Subject: management
### Type: config
## Cause: threshold-crossed
### Child Action: 
### Code: F112296
### Count: 22
### Description: Threshold crossing alert for class l2IngrPktsPart5min, property dropRate
### DN: fltcode-F112296
### Domain: infra
### Non
#### Acknowledged: 22
#### Delegated: 0
#### Delagated And Acknowledged: 0
### Rule: tca-l2-ingr-pkts-part5min-drop-rate
### Severity: warning
### Status: 
### Subject: counter
### Type: operational
## Cause: oper-state-change
### Child Action: 
### Code: F4149
### Count: 1
### Description: This fault occurs when you remove LC/FM/SUP/SC from the slot
### DN: fltcode-F4149
### Domain: infra
### Non
#### Acknowledged: 1
#### Delegated: 1
#### Delagated And Acknowledged: 1
### Rule: eqpt-slot-oper-st-change
### Severity: minor
### Status: 
### Subject: lc-fm-sup-sc-removed
### Type: operational
## Cause: threshold-crossed
### Child Action: 
### Code: F100264
### Count: 20
### Description: Threshold crossing alert for class eqptIngrDropPkts5min, property bufferRate
### DN: fltcode-F100264
### Domain: infra
### Non
#### Acknowledged: 20
#### Delegated: 20
#### Delagated And Acknowledged: 20
### Rule: tca-eqpt-ingr-drop-pkts5min-buffer-rate
### Severity: warning
### Status: 
### Subject: counter
### Type: operational
## Cause: configuration-failed
### Child Action: 
### Code: F0764
### Count: 1
### Description: This fault occurs when a logical device is being configured in a way which is not compatible with the meta device information supplied by the device package.
### DN: fltcode-F0764
### Domain: tenant
### Non
#### Acknowledged: 1
#### Delegated: 1
#### Delagated And Acknowledged: 1
### Rule: vns-aldev-conf-mismatch
### Severity: minor
### Status: 
### Subject: management
### Type: config
## Cause: port-down
### Child Action: 
### Code: F0104
### Count: 1
### Description: This fault occurs when a bond interface on a controller is in the link-down state.
### DN: fltcode-F0104
### Domain: infra
### Non
#### Acknowledged: 1
#### Delegated: 1
#### Delagated And Acknowledged: 1
### Rule: cnw-aggr-if-down
### Severity: critical
### Status: 
### Subject: equipment
### Type: operational
## Cause: resolution-failed
### Child Action: 
### Code: F0956
### Count: 2
### Description: The object refers to an object that was not found.
### DN: fltcode-F0956
### Domain: infra
### Non
#### Acknowledged: 2
#### Delegated: 2
#### Delagated And Acknowledged: 2
### Rule: fv-rs-dom-att-resolve-fail
### Severity: warning
### Status: 
### Subject: relation-resolution
### Type: config
## Cause: resolution-failed
### Child Action: 
### Code: F1003
### Count: 1
### Description: The object refers to an object that was not found.
### DN: fltcode-F1003
### Domain: infra
### Non
#### Acknowledged: 1
#### Delegated: 1
#### Delagated And Acknowledged: 1
### Rule: infra-rs-dom-presolve-fail
### Severity: warning
### Status: 
### Subject: relation-resolution
### Type: config
## Cause: configuration-failure
### Child Action: 
### Code: F0721
### Count: 1
### Description: This fault is raised when a VLAN/VxLAN/NVGRE pool cannot be deployed due to a missing or invalid configuration.
### DN: fltcode-F0721
### Domain: infra
### Non
#### Acknowledged: 1
#### Delegated: 1
#### Delagated And Acknowledged: 1
### Rule: fvns-ainst-pconfig-failed
### Severity: minor
### Status: 
### Subject: infra-policy
### Type: config
## Cause: threshold-crossed
### Child Action: 
### Code: F96976
### Count: 20
### Description: Threshold crossing alert for class eqptEgrDropPkts5min, property errorRate
### DN: fltcode-F96976
### Domain: infra
### Non
#### Acknowledged: 20
#### Delegated: 20
#### Delagated And Acknowledged: 20
### Rule: tca-eqpt-egr-drop-pkts5min-error-rate
### Severity: warning
### Status: 
### Subject: counter
### Type: operational
## Cause: configuration-failed
### Child Action: 
### Code: F1298
### Count: 4
### Description: This fault occurs when deliverying EPg policies to a node has failed
### DN: fltcode-F1298
### Domain: tenant
### Non
#### Acknowledged: 4
#### Delegated: 2
#### Delagated And Acknowledged: 2
### Rule: fv-pol-delivery-status-configuration-failed
### Severity: minor
### Status: 
### Subject: epg
### Type: config
## Cause: threshold-crossed
### Child Action: 
### Code: F96760
### Count: 20
### Description: Threshold crossing alert for class eqptEgrDropPkts5min, property bufferRate
### DN: fltcode-F96760
### Domain: infra
### Non
#### Acknowledged: 20
#### Delegated: 20
#### Delagated And Acknowledged: 20
### Rule: tca-eqpt-egr-drop-pkts5min-buffer-rate
### Severity: warning
### Status: 
### Subject: counter
### Type: operational
## Cause: threshold-crossed
### Child Action: 
### Code: F100480
### Count: 20
### Description: Threshold crossing alert for class eqptIngrDropPkts5min, property errorRate
### DN: fltcode-F100480
### Domain: infra
### Non
#### Acknowledged: 20
#### Delegated: 20
#### Delagated And Acknowledged: 20
### Rule: tca-eqpt-ingr-drop-pkts5min-error-rate
### Severity: warning
### Status: 
### Subject: counter
### Type: operational
## Cause: threshold-crossed
### Child Action: 
### Code: F112425
### Count: 4
### Description: Threshold crossing alert for class l2IngrPktsAg15min, property dropRate
### DN: fltcode-F112425
### Domain: infra
### Non
#### Acknowledged: 4
#### Delegated: 4
#### Delagated And Acknowledged: 4
### Rule: tca-l2-ingr-pkts-ag15min-drop-rate
### Severity: warning
### Status: 
### Subject: counter
### Type: operational
## Cause: threshold-crossed
### Child Action: 
### Code: F103824
### Count: 1
### Description: Threshold crossing alert for class eqptTemp5min, property normalizedLast
### DN: fltcode-F103824
### Domain: infra
### Non
#### Acknowledged: 1
#### Delegated: 1
#### Delagated And Acknowledged: 1
### Rule: tca-eqpt-temp5min-normalized-last
### Severity: critical
### Status: 
### Subject: counter
### Type: operational
## Cause: threshold-crossed
### Child Action: 
### Code: F100696
### Count: 20
### Description: Threshold crossing alert for class eqptIngrDropPkts5min, property forwardingRate
### DN: fltcode-F100696
### Domain: infra
### Non
#### Acknowledged: 20
#### Delegated: 20
#### Delagated And Acknowledged: 20
### Rule: tca-eqpt-ingr-drop-pkts5min-forwarding-rate
### Severity: warning
### Status: 
### Subject: counter
### Type: operational