import configparser

# CREATE OBJECT
config_file = configparser.ConfigParser()

# ADD SECTION
config_file.add_section("TPS")
# ADD SETTINGS TO SECTION
config_file.set("TPS", "tps", "1000")

config_file.add_section("DBdetails")
config_file.set("DBdetails", "host", "10.200.123.110")
config_file.set("DBdetails", "port", '3306')
config_file.set("DBdetails", "user", "root")
config_file.set("DBdetails", "password", "$Witch@@1133")
config_file.set("DBdetails", "database", "mydatabase")
config_file.set("DBdetails", "charset", "utf8")



# SAVE CONFIG FILE
with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print("Config file 'configurations.ini' created")

# PRINT FILE CONTENT
read_file = open("configurations.ini", "r")
content = read_file.read()
print("Content of the config file are:\n")
print(content)
read_file.flush()
read_file.close()