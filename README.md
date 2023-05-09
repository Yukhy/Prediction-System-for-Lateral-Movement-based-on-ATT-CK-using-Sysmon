# Prediction System for Lateral Movement Based on ATT&CK Using Sysmon

## Overview
This is a powerful tool that helps organizations quickly detect and understand malicious activity within their networks. By converting Windows logs collected by Sysmon into MITRE ATT&CK techniques, security teams can quickly visualize and identify attack patterns and progress. 

## Description
For a detailed description, please see [here](https://github.com/Yukhy/Prediction-System-for-Lateral-Movement-based-on-ATT-CK-using-Sysmon/blob/main/docs/description_slide.pdf).

## Features
- Convert Sysmon logs to MITRE ATT&CK techniques
- Visualize converted data in list format or ATT&CK matrix format
- Predict Lateral Movement of each device from Sysmon logs of multiple devices

## Requirements
- Docker <= 20.10.24

## Install
1. Clone the repository
```
$ git clone git clone https://github.com/Yukhy/prediction-system-for-lateral-movement-based-on-att-ck-using-sysmon.git

```

2. Navigate to the project directory
```
$ cd prediction-system-for-lateral-movement-based-on-att-ck-using-sysmon
```
3. Store data in the database
※ Please see here for details on the database.
```
$ docker compose -f docker-compose.local.yml run operation python seed.py
```

4. Launch the container with Docker
```
$ docker compose -f docker-compose.local.yml up -d
```

5. Access in the browser
Access ```localhost:8000```

## Usage
For detailed usage instructions, please see [here](https://github.com/Yukhy/Prediction-System-for-Lateral-Movement-based-on-ATT-CK-using-Sysmon/blob/main/docs/usage.md).

## Disclamer
This project is for research purposes, and does not provide any guarantees regarding the completeness and accuracy of the source code and its contents. We are not responsible for any direct or indirect loss caused by using the information or tools contained on this page.
