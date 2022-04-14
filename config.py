import pickle
from config_class import config

pickle_obj = open('configuration.pickle', 'rb')
config_obj = pickle.load(pickle_obj)


while True:
    print("Select the configuration to change:\n")
    print("1.Save/Change userid and password.")
    print("2.Change to Listen Only Mode/Microphone Mode.")
    print("3.Poll Option Selection Manual Mode/Bot Mode.")

    config_option = input("\nEnter the option number(1/2/3): ")

    if config_option == '1':
        print("\nProvided userid and password will be used for future login.\n")
        config_obj.userid = input("Userid: ")
        config_obj.password = input("Password: ")

    elif config_option == '2':
        print("\nClass will be joined using selected mode.\n")
        print('1.Listen Only Mode.')
        print("2.Microphone Mode.")
        config_obj.listen_mode = input("Choose mode(1/2): ")

    elif config_option == '3':
        print("\nPoll questions will be answered using the selected mode.\n")
        print("1.Let the bot answer the poll questions.")
        print("2.No, I will answer myself.")
        config_obj.poll_mode = input("\nChoose mode(1/2): ")


    else:
        print("\nSelect valid option.")
        continue

    done_op = input("\nStill have something to change? Press Enter or 'n'.(Enter/n)")

    if done_op == 'n':
        break
    
pickle_obj.close()
config_obj = config()
pickle_obj = open("configuration.pickle", 'wb')
pickle.dump(config_obj, pickle_obj)

