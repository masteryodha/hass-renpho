# Renpho Weight

This is a custom component to import weight and last weigh time from the Renpho app into Home Assistant.

### Installation

Copy this folder to `<config_dir>/custom_components/renpho_weight/`.


### Configuration

- `email` is **mandatory** and represent the email you use to log in the app
- `password` is **mandatory** and represent the password you use to log in the app
- `refresh` is **optional** and represent the time to check for update. 
- `weight_units` is **optional** and represent the unit of every MASS sensor.  Possible values are 'kg' or 'lb'.

For example, add the following entry in your `configuration.yaml`:

```yaml
renpho_weight:
  email: <email address>
  password: <password>
  refresh: 600
  weight_units: [kg | lb]

sensor:
  platform: renpho_weight
```


### Important information
- Bear in mind everytime you log in it logs you out of the app, so in my example it gives me ten minutes (660 seconds) between checking in case I ever wish to browse the app.
- The MASS data are stored in Kg on the renpho API.  So, if you select the weight_units, in lb, a conversion will be made by a factor of 2.2046226218


### RoadMap / What's to come
- Get All the users and create sensor for all of them
- Specify in the config which users to get
- Don't get logged out of mobile app when connecting via this python