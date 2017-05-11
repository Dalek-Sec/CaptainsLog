###############################
# Imports
import time
import json
import glob
import os

###############################
# Constants
# ENTER PATH TO SAVE FOLDER HERE
LOG_FILES_PATH = ""

###############################
# Functions used once (in expected order called)
def main():
    """Runs main program"""
    tags = tags_prompt()
    while True:
        print_previous_messages(tags)
        new_message_prompt(tags)

def tags_prompt():
    tags = []
    print ("Enter tags for this session. Enter a number to add a recent set. "
           + "Return empty when finished.")
    recent_messages = get_previous_messages([], slice(-5, None))
    tag_presets = recent_tags(recent_messages)
    print_tag_presets(tag_presets)
    while True:
        tag = raw_input()
        if tag == "":
            print "Finished entering tags. " + str(tags)
            break
        else:
            try:
                tag_preset_index = int(tag)
                tags += list(tag_presets[tag_preset_index])
                print "Added set: " + list(tag_presets[tag_preset_index])
            except ValueError:
                tags.append(tag)

            print "Added tag: " + tag

    return tags

def recent_tags(messages):
    """Gets all unique sets of tags used in passed messages"""
    tag_sets = [tuple(message[1]['tags']) for message in messages]
    tag_sets = list(set(tag_sets))
    return tag_sets

def print_tag_presets(tag_presets):
    """Prints passed presets in a readable form beside their corrosonding index"""
    for index, tag_preset in enumerate(tag_presets):
        print str(index) + "|" + str(tag_preset)

def print_previous_messages(tags):
    print "\n" + "=" * 32
    previous_messages = get_previous_messages(tags, slice(-5, None))
    print_messages(previous_messages)
    print "Tags: " + str(tags)

def print_messages(messages):
    """Formats and prints passed messages"""
    for message in messages:
        print time.asctime(time.localtime(message[0])) + "|" + message[1]["log_entry"]

def new_message_prompt(tags):
    log_entry = raw_input("Enter log message:")
    log_key = str(time.time())
    file_name = time.strftime("%Y%m%d", time.gmtime())
    save_log_entry(log_entry, log_key, file_name, tags)

def save_log_entry(log_entry, log_entry_key, file_name, tags):
    """Saves log entry in a file at LOG_FILES_PATH."""
    save_path = os.path.join(LOG_FILES_PATH, file_name + ".json")
    log = load_log_file(save_path)
    log[log_entry_key] = {"log_entry":log_entry, "tags":tags}

    with open(save_path, "w") as log_file:
        json.dump(log, log_file, indent=4)

###############
# Functions used more than once (in expected order first called)
def get_previous_messages(wanted_message_tags, wanted_days):
    """Returns messages with timestamps
       from wanted days (represented by a slice) and all wanted tags."""
    file_paths = glob.glob(LOG_FILES_PATH + "*")
    file_paths.sort()
    file_paths = file_paths[wanted_days]
    wanted_messages = []
    for file_path in file_paths:
        log = load_log_file(file_path)
        for key in log:
            if set(wanted_message_tags).issubset(log[key]["tags"]):
                wanted_messages.append((float(key), log[key]))

    wanted_messages.sort()
    return wanted_messages

def load_log_file(file_path):
    """Returns extracted log from requested file. If file does not exist it is created"""
    try:
        with open(file_path) as log_file:
            log = json.load(log_file)

    except IOError:
        with open(file_path, "w") as log_file:
            log = {}

    return log

if __name__ == '__main__':
    main()
