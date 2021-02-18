# JS8CLI
### A JS8Call command line utility.

## Background
This simple utility is designed to facilitate updating JS8Call's location and to facilitate sending APRS SMS and grid location messages to spotters. This utiity can also be used to automatically update JS8Call's location as well as automatically send grid beaons to APRS-IS via spotters.

## Requirements
- Python 3 (Tested with Python 3.8)
- PIP installed
- GPSD installed and running
- JS8Call installed and running
- JS8Call's TCP or UDP API should be enabled in the configuration.

## Setup

To set the project up copy it to a folder such as `/opt/threesixes/js8cli` and add that folder to your `PATH` variable so you can use it on the CLI. As the user the project will run as execute `pip3 install -r requirements.txt`. This will install the necessary Python libraries.

You should then edit copy the distributed configuration file as the proper config the application will use: `cp js8cli.dist.json js8cli.json`.

Now edit the file. You can modify any of the following properties. The defaults are at the end of this README:

- `aprs_loc_update_min`: This triggers APRS updates in minutes. `0` disables updates.
- `gpsd_host`: This is the host that's running GPSD. It's typically `127.0.0.1`.
- `gpsd_port`: This is the port that's running GPSD. It's typically `2947`.
- `grid_level`: The accuracy of the Maidenhead grid square to use with JS8Call. Accepts `1`-`5`, 1 being a 2 character grid square locator and 5 being a 10 character grid square.
- `js8call_host`: The host JS8Call is running on. This is typically `127.0.0.1`.
- `js8call_loc_refresh_min`: How many minutes between JS8Call location updates?
- `js8call_port`: The port JS8Call is running on.
- `js8call_proto`: The protocol being used by the JS8Call API. Can be `tcp` or `udp`.


## How to use as a CLI utility
### To update JS8Call's grid square location based on GPS location:

`js8cli setgrid`

Optional arguments:

`--grid n` where n is the accuracy of the maidenhead grid squiare used: 1-5. Ex: 1 will give a maidenhead position of `AA`. Providing 2 will provide `AA11`, 4 will provide `AA11aa11`.

### To send your grid location to APRS via a spotter:

`js8cli aprsgrid`

Optional arguments:

`--grid n` where n is the accuracy of the maidenhead grid squiare used: 1-5. Ex: 1 will give a maidenhead position of `AA`. Providing 2 will provide `AA11`, 4 will provide `AA11aa11`.

`-d` prevents JS8Call from sending the message allowing the user to choose when to send it.

### To send an SMS via APRS using SMSGTE:

`js8cli aprssms --to 5555555555 --msg "Hello, world."`

Where `--to` specifies a phone number or [smsgte.org](https://smsgte.org) alias, and `--msg` is the message content or shortcut you wish to send.

Optional arguments:

`-d` prevents JS8Call from sending the message allowing the user to choose when to send it.


## Automatically updating JS8Call location and/or APRS grid location periodically.

This is accomplished by either exeuting `js8cli daemon` or by copying the systemd configuration file into place, enabling and starting it after configuring `aprs_loc_update_min` and `js8call_loc_refresh_min` in `js8cli.json`. These settings configure the timing of APRS location updates in minutes and the JS8Call location updates from the GPS in minutes as well.

After the configuration file has been modified the systemd unit can be copied into place and set up using the following commands:

```bash
sudo cp util/js8cli.service /etc/systemd/system
```

Edit the systemd unit file at `/etc/systemd/system/js8cli.service` with your favorite editor. Set the `User` parameter to a user with access to the path the project is run in. This example assumes you've installed the project folder and configuration in `/opt/threesixes`. If that's not the case change the working directory and path to the project.

```
sudo systemctl enable js8cli
sudo systemctl start js8cli
```

### Default configuration
```json
{
  "aprs_loc_update_min": 0,
  "gpsd_host": "127.0.0.1",
  "gpsd_port": 2947,
  "grid_level": 5,
  "js8call_host": "127.0.0.1",
  "js8call_loc_refresh_min": 5,
  "js8call_port": 2442,
  "js8call_proto": "tcp"
}
```