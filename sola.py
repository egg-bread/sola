#!/usr/bin/env python

'''
  File name: sola.py
  Author: tofubridge
  Description: sola reads daemon data in from a json file and writes the data
  to a csv file for easier data manipulation
  Python Version: 3.6.4
'''

## ========================== Import libraries =================================
import json
import csv
import os

## =========================== Useful classes ==================================
class Daemon:
    '''Fields: daemon, card_desc, skill_name, skill_desc, skill_quote, summon_quote, 
               lb_quote, ability1_name, ability2_name, ability1_desc, ability2_desc,
               daemon_type, special_bond        
       where all fields are Str'''
    
    def __init__(self, daemon, card_desc=None, skill_name=None, skill_desc=None,\
                 skill_quote=None, summon_quote=None, lb_quote=None,\
                 ability1_name=None, ability2_name=None, ability1_desc=None,\
                 ability2_desc=None, daemon_type=None, special_bond=None):
        self.daemon = daemon
        self.card_desc = not_found if card_desc is None else card_desc
        self.skill_name = not_found if skill_name is None else skill_name
        self.skill_desc = not_found if skill_desc is None else skill_desc
        self.skill_quote = not_found if skill_quote is None else skill_quote
        self.summon_quote = not_found if summon_quote is None else summon_quote
        self.lb_quote = not_found if lb_quote is None else lb_quote
        self.ability1_name = na if ability1_name is None else ability1_name
        self.ability2_name = na if ability2_name is None else ability2_name
        self.ability1_desc = na if ability1_desc is None else ability1_desc
        self.ability2_desc = na  if ability2_desc is None else ability2_desc
        self.daemon_type = not_found if daemon_type is None else daemon_type
        self.special_bond = na if special_bond is None else special_bond
     
    def __repr__(self):
        display = "Name: {0}\nType: {1}\nSpecial Bond: {2}\nSkill Name: {3}\n"+\
            "Ability1 Name: {4}\nAbility2 Name: {5}"
        return display.format(self.daemon, self.daemon_type, self.special_bond,\
                              self.skill_name, self.ability1_name, self.ability2_name)
    


##==================== Useful constants and variables ==========================

na = "N/A"
not_found = "Not found."
ranged = "Ranged" # one of daemon_type
melee = "Melee" # one of daemon_type
healer = "Healer" # one of daemon_type
max_hp = "max HP"
skill_dmg = "skill DMG"
normal_atk = "normal ATK"
placeholder = "{#MonsterName#"

# dictionary to store all daemons from json file
daemon_dictionary = {} 


## ======================== Helper function(s) =================================

# check_key(key, d) returns the value at d[key] if key is in d and None otherwise  
# check_key: Str (dictof Daemon) -> (anyof Str None)

def check_key(key,d):
    if key in d:
        return d[key]
    else:
        return None


# d_type(daemons) mutates the value for each key in daemons to update the
#                 daemon_type field if required
# d_type: (dictof Daemon) -> (dictof Daemon)

def d_type(daemons):
    for key in daemons:
        dt = daemons[key].daemon_type
        if max_hp in dt:
            daemons[key].daemon_type = healer
        elif skill_dmg in dt:
            daemons[key].daemon_type = ranged
        elif normal_atk in dt:
            daemons[key].daemon_type = melee
        else:
            daemons[key].daemon_type = dt


# replacer(daemons) mutates the value for each key in daemons to update the
#                   special_bond, card_desc, abiity1_desc, ability2_desc field(s)
#                   if required
# replacer: (dictof Daemon) -> (dictof Daemon)

def replacer(daemons):
    for key in daemons:
        # fields to access
        bond = daemons[key].special_bond
        c_desc = daemons[key].card_desc
        ab1_desc = daemons[key].ability1_desc
        ab2_desc = daemons[key].ability2_desc
        
        if placeholder in bond:
            start = bond.find("{")
            end =  bond.find("}")
            full_placeholder = bond[start:end+1]
            daemon_id_to_replace = \
                "".join(list(filter(lambda c: c.isdigit(), full_placeholder)))
            daemon_id_name = daemons[daemon_id_to_replace].daemon
            daemons[key].special_bond = bond.replace(full_placeholder, daemon_id_name)
        else:
            daemons[key].special_bond = bond
        
        if placeholder in c_desc:
            start = c_desc.find("{")
            end =  c_desc.find("}")
            full_placeholder = c_desc[start:end+1]
            daemon_id_to_replace = \
                "".join(list(filter(lambda c: c.isdigit(), full_placeholder)))
            daemon_id_name = daemons[daemon_id_to_replace].daemon
            daemons[key].card_desc = c_desc.replace(full_placeholder, daemon_id_name)
        else:
            daemons[key].card_desc = c_desc
        
        if placeholder in ab1_desc:
                start = ab1_desc.find("{")
                end =  ab1_desc.find("}")
                full_placeholder = ab1_desc[start:end+1]
                daemon_id_to_replace = \
                    "".join(list(filter(lambda c: c.isdigit(), full_placeholder)))
                daemon_id_name = daemons[daemon_id_to_replace].daemon
                daemons[key].ability1_desc = ab1_desc.replace(full_placeholder, daemon_id_name)
        else:
            daemons[key].ability1_desc = ab1_desc    
       
        if placeholder in ab2_desc:
                start = ab2_desc.find("{")
                end =  ab2_desc.find("}")
                full_placeholder = ab2_desc[start:end+1]
                daemon_id_to_replace = \
                    "".join(list(filter(lambda c: c.isdigit(), full_placeholder)))
                daemon_id_name = daemons[daemon_id_to_replace].daemon
                daemons[key].ability2_desc = ab2_desc.replace(full_placeholder, daemon_id_name)
        else:
            daemons[key].ability2_desc = ab2_desc 
 
    
## ========================= Main Program  =====================================

# ask user for the json file to read in the daemon information
user_input = input("Enter json file name: ")

# check if file actually exists or user entered faulty name
valid_input = os.path.isfile(user_input + ".json")

while valid_input == False:
    print("File does not exist.")
    user_input = input("Enter json file name: ")
    valid_input = os.path.isfile(user_input + ".json")


# load all data in from json file, making sure encoding is correct 
with open(user_input + ".json", "r", encoding="utf-8") as reader:
    data = json.load(reader)

# get all necessary data from the json file    
data_bundle = data["bundles"]

# get daemon id
daemon_id = sorted(data_bundle["MonsterName"]["strings"].keys())

# get daemon name, description, type
daemon_name = data_bundle["MonsterName"]["strings"]
daemon_desc = data_bundle["MonsterDesc"]["strings"]
daemon_type_bonds = data_bundle["monster_entanglement"]["strings"]

# get daemon skill info: name, description, quote
daemon_skill_name = data_bundle["MonsterSkillName"]["strings"]
daemon_skill_desc = data_bundle["MonsterSkillDesc"]["strings"]
daemon_skill_quote = data_bundle["MonsterSkillLine"]["strings"]

# get daemon ability info (there can be None, 1 and/or 2 abilities)
daemon_ability_desc = data_bundle["MonsterAbilityDesc"]["strings"]
daemon_ability_name = data_bundle["MonsterAbilityName"]["strings"]

# get daemon summon and limit break quote
daemon_summon_quote = data_bundle["MonsterFirstObtain"]["strings"]
daemon_lb_quote = data_bundle["MonsterAwakening"]["strings"]

# add daemons to daemon_dictionary
for num in daemon_id:
    ab1_num = num + "01"
    ab2_num = num + "02"
    daemon_dictionary[num] = Daemon(daemon_name[num], check_key(num, daemon_desc),\
                                    check_key(num, daemon_skill_name),\
                                    check_key(num, daemon_skill_desc),\
                                    check_key(num, daemon_skill_quote),\
                                    check_key(num, daemon_summon_quote),\
                                    check_key(num, daemon_lb_quote),\
                                    check_key(ab1_num, daemon_ability_name),\
                                    check_key(ab2_num, daemon_ability_name),\
                                    check_key(ab1_num, daemon_ability_desc),\
                                    check_key(ab2_num, daemon_ability_desc),\
                                    check_key(ab1_num, daemon_type_bonds),\
                                    check_key(ab2_num, daemon_type_bonds))

# mutate type field in daemon_dictionary to the proper daemon type if required
d_type(daemon_dictionary)

# mutate fields for each Daemon in daemon_dictionary if required
replacer(daemon_dictionary)


# ask user for file to write to
user_output = input("Enter file name to write daemon information to: ")

# check if file already exists to prevent user from overwriting that file
valid_output = os.path.isfile(user_output + ".csv")

while valid_output == True:
    print("File already exists!")
    user_output = input("Enter file name to write daemon information to: ")
    valid_output = os.path.isfile(user_output + ".csv")

# check if filename contains forbidden characters
forbidden = ["/", "<", ">", ":", '"', "\\", "/", "|", "?", "*"]
forbidden_ending = [" ", "."]

while user_output == "" or any(i in user_output for i in forbidden) or \
      user_output[-1] in forbidden_ending:
    print("Yikes! That's not a friendly filename!")
    user_output = input("Enter file name to write daemon information to: ")


# open a csv file for writing information from daemon_dictionary
with open(user_output + ".csv", "w", encoding="utf-8-sig") as csvfile:
    
    # csv header values
    fn = ["id","Daemon","Type", "Special Bond", "Card Desc", "LB Quote", "Summon Quote",\
          "Skill Quote", "Skill Name","Skill Desc","Ability1 Name",\
          "Ability1 Desc","Ability2 Name", "Ability2 Desc"]
    
    # set up csv file and begin writing
    writer = csv.DictWriter(csvfile, fieldnames=fn)
    writer.writeheader()
    for k in daemon_dictionary:
        writer.writerow({"id": "{0}".format(k),\
                         "Daemon": "{0}".format(daemon_dictionary[k].daemon),\
                         "Type": "{0}".format(daemon_dictionary[k].daemon_type),\
                         "Special Bond": "{0}".format(daemon_dictionary[k].special_bond),\
                         "Card Desc": "{0}".format(daemon_dictionary[k].card_desc),\
                         "LB Quote": "{0}".format(daemon_dictionary[k].lb_quote),\
                         "Summon Quote": "{0}".format(daemon_dictionary[k].summon_quote),\
                         "Skill Quote": "{0}".format(daemon_dictionary[k].skill_quote),\
                         "Skill Name": "{0}".format(daemon_dictionary[k].skill_name),\
                         "Skill Desc": "{0}".format(daemon_dictionary[k].skill_desc),\
                         "Ability1 Name": "{0}".format(daemon_dictionary[k].ability1_name),\
                         "Ability1 Desc": "{0}".format(daemon_dictionary[k].ability1_desc),\
                         "Ability2 Name": "{0}".format(daemon_dictionary[k].ability2_name),\
                         "Ability2 Desc": "{0}".format(daemon_dictionary[k].ability2_desc),})

print("sola has finished writing to '{0}'".format(user_output+".csv"))