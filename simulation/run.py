from chord import Chord
chord = Chord()


if __name__ == "__main__":
    while(True):
        print(chord.ring)
        print("************************MENU*************************")
        print("PRESS ***********************************************")
        print("1. Add a node *****************************************")
        print("2. Delete a node ******************************************")
        print("3. Enter a node *****************************************")
        print("0. EXIT ******************************************")
        print("*****************************************************")
        choice = input()

        if(choice == '1'):
            port = input("ENTER THE port : ")
            ExistingNodePort = None
            if chord.ring != {}:
                ExistingNodePort = input("ENTER THE EXISTING NODE PORT (if any): ")
            chord.addNode(port, ExistingNodePort)
            # print(f"Add node id {id} to the chord")
            continue

        elif(choice == '2'):
            port = input("ENTER THE port : ")
            chord.deleteNode(port)
            print(f"Node with port {port} has been deleted")
            continue

        elif(choice == '3'):
            chord.enterNode(input("ENTER THE port : "))
            continue

        elif(choice == '0'):
            print("bye~")
            exit()
            
        else:
            print("INCORRECT CHOICE")
            continue