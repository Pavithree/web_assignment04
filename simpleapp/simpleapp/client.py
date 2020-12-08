from users_db import count_users
import requests
import matplotlib.pyplot as plt
import datetime
import sys

# def register(contact, url) : Makes a post request to localhost/form
#                            : Returns status, count of entries in the database and associated msg
def register(contact, url):

  user = contact.split(',')[0]
  email = contact.split(',')[1]
  contacts_list = {"name": user,
                   "email": email,
                   }

  status = requests.post(url, contacts_list)
  if status.status_code == 200:
      msg = "Success! You have added a new contact to the list."
  else:
      msg = status.reason

  list_size = f"{count_users()}"
  data={"list_size": list_size, "msg": msg}
  return (status,data)


# def read_file(fname): returns the content of the file
def read_file(fname):
    return open(fname,"r")


#def parse_response(text) : parses the content from text and returns list size and msg
def parse_response(text):
    return (text['list_size'],text['msg'])


# function to get the timeline plot
def plot_timeline(timeline, fname):
    time = []
    count = []
    for keys in timeline:
        time.append(keys)
        count.append(timeline[keys])

    figure = plt.figure()
    plt.plot(time,count)
    plt.xlabel("Timestamp")
    plt.ylabel("List size")
    plt.xticks(rotation=90)
    plt.savefig(fname)
    plt.show()


# function to get the bar plot
def plot_bar(success_count,error_count,output_fileBar):
    fig, ax = plt.subplots()
    width = 0.25
    rects1 = ax.bar(1 - width / 2, success_count, width, color="green",
                    label='Success Count')
    rects2 = ax.bar(1 + width / 2, error_count, width, color="red",
                    label='Error Count')
    ax.set_ylabel('Frequency')
    ax.set_title('Server Responses')
    ax.legend()

    fig.tight_layout()
    plt.savefig(output_fileBar)
    plt.show()


#main function
if __name__ == '__main__':
    timeline = []
    count = []
    error_count = 0
    success_count = 0
    contacts_count = 0
    URL = "http://localhost:5000/form"
    fname = sys.argv[1]
    contacts = read_file(fname)
    for contact in contacts:
        contacts_count +=1
        status, text = register(contact=contact, url=URL)
        s = datetime.datetime.now().strftime("%H:%M:%S")
        timeline.append(s)
        print(f"Status code from the app {status}")
        print(f"Text is {text}")
        list_size, contains_success_msg = parse_response(text)
        count.append(list_size)
        if status.status_code == 200:
            success_count += 1
        else:
            error_count += 1

    list_sizes = dict(zip(timeline,count))
    total_request = contacts_count
    assert error_count + success_count == total_request
    output_file = "list_size_timeline.png"
    plot_timeline(list_sizes, output_file)
    output_fileBar = "results.png"
    plot_bar(success_count, error_count, output_fileBar)


