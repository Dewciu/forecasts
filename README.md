# Simple Forecast Application

This is simple weather forecast application for particular latitude and longitude.
Module takes data from system .xml files and saving forecasts for each in separate .xml files.
Weather forecast information is provided via https://developer.accuweather.com

## Requirements

* Python 3.10.5
* Virtualenv

## Installation

Create virtual environment using virtualenv.

```bash
virtualenv venv
```

Install all the requirements from requirements.txt file.

```bash
pip install -r requirements.txt
```

Create account on https://developer.accuweather.com and get the API key.

Paste key in api_keys/api_key.xml to the 'key' attribute.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<api_key key='YOUR KEY'>
</api_key>
```

## Usage

If you want to start the program, you will need to type this command sentence.

```bash
python src/main.py <input_file_path> <output_file_path> <mode>
```

* **Input file path** is the folder where system .xml files are stored.
* **Output file path** is the folder, where output forecasts for each system are stored. You can provide single file, then just one file will be processed.
* All file paths should be **relative**.
* Possible **modes**: -c [*continous*], -s [*single_time*]

Use continous mode when you want to create single thread for each file in input path.
Each system .xml file can provide optional parameter "update_period" which defines a forecast refresh time.

### Example usage

Single file data in single time mode from folder 'systems' to folder 'forecasts':

```bash
python src/main.py systems/system1.xml forecasts -s
```

Multiple file data in single time mode from folder 'systems' to folder 'forecasts':

```bash
python src/main.py systems forecasts -s
```

Single file data in continous mode from folder 'systems' to folder 'forecasts':

```bash
python src/main.py systems/system1.xml forecasts -c
```

Multiple file data in continous mode from folder 'systems' to folder 'forecasts':

```bash
python src/main.py systems forecasts -c
```


#### Example input

```xml
<?xml version="1.0" encoding="UTF-8"?>
<system xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    UUID="00000000-0000-2000-8000-00805F9B34FB" name="" description=""
    >
    <component UID="0df319f4-9d79-4e4f-b5c5-df1c28b49f57" name="A" longitude="-21.90" latitude="64.13">
    </component>    
    <component UID="4f7cb3c5-d2d7-472e-8b13-0b66437e35a0" name="B" longitude="-18.09" latitude="65.68">
    </component>
    <component UID="7e290402-ebab-4e77-9ea9-b8e8f9727302" name="C" longitude="-14.40" latitude="65.26">
    </component>
</system>
```

#### Example output

```xml
<?xml version="1.0" encoding="utf-8"?>
<system xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" UUID="00000000-0000-2000-8000-00805F9B34FB">
	<component UID="0df319f4-9d79-4e4f-b5c5-df1c28b49f57">
		<model_parameters>
			<dynamic>
				<time_sequence sequence_type="temperature" base_time="2022-09-05T22:37:08" rel_time="21:00:00 22:00:00 23:00:00 00:00:00 01:00:00 02:00:00 03:00:00 04:00:00 05:00:00 06:00:00 07:00:00 08:00:00" data="11 11 10 10 10 10 10 8 9 9 9 11"></time_sequence>
				<time_sequence sequence_type="day_light" base_time="2022-09-05T22:37:08" rel_time="21:00:00 22:00:00 23:00:00 00:00:00 01:00:00 02:00:00 03:00:00 04:00:00 05:00:00 06:00:00 07:00:00 08:00:00" data="false false false false false false false false false false true true"></time_sequence>
			</dynamic>
		</model_parameters>
	</component>
	<component UID="4f7cb3c5-d2d7-472e-8b13-0b66437e35a0">
		<model_parameters>
			<dynamic>
				<time_sequence sequence_type="temperature" base_time="2022-09-05T22:37:08" rel_time="21:00:00 22:00:00 23:00:00 00:00:00 01:00:00 02:00:00 03:00:00 04:00:00 05:00:00 06:00:00 07:00:00 08:00:00" data="11 11 10 10 10 10 10 8 9 9 9 11"></time_sequence>
				<time_sequence sequence_type="day_light" base_time="2022-09-05T22:37:08" rel_time="21:00:00 22:00:00 23:00:00 00:00:00 01:00:00 02:00:00 03:00:00 04:00:00 05:00:00 06:00:00 07:00:00 08:00:00" data="false false false false false false false false false false true true"></time_sequence>
			</dynamic>
		</model_parameters>
	</component>
	<component UID="7e290402-ebab-4e77-9ea9-b8e8f9727302">
		<model_parameters>
			<dynamic>
				<time_sequence sequence_type="temperature" base_time="2022-09-05T22:37:08" rel_time="21:00:00 22:00:00 23:00:00 00:00:00 01:00:00 02:00:00 03:00:00 04:00:00 05:00:00 06:00:00 07:00:00 08:00:00" data="11 11 10 10 10 10 10 8 9 9 9 11"></time_sequence>
				<time_sequence sequence_type="day_light" base_time="2022-09-05T22:37:08" rel_time="21:00:00 22:00:00 23:00:00 00:00:00 01:00:00 02:00:00 03:00:00 04:00:00 05:00:00 06:00:00 07:00:00 08:00:00" data="false false false false false false false false false false true true"></time_sequence>
			</dynamic>
		</model_parameters>
	</component>
</system>
```


### Deploy on Docker

If you want to deploy this application on Docker, you have all setup prepared.
All you need to do is build the image from Dockerfile.


```baah
docker image build --tag forecasts .
```

Docker Compose was used becouse of volumes, which give us a possibility to change processed XML data in the container.
Everything you put in the systems repository folder, will be processed in the container. The same with API key.

```bash
docker-compose up -d
```