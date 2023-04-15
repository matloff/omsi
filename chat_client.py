import socket
import sys
import threading
import tkinter


def query(server_addr, port, my_question):
    try:
        soc = socket.socket()
        soc.connect((server_addr, port))
        soc.send(str.encode(my_question))
        msg_received = soc.recv(1024).decode()
        soc.close()
    except Exception as e:
        msg_received = str(e)
    return msg_received


def gui_setup():
    # Acquire Server info
    server_addr = sys.argv[1]
    port = int(sys.argv[2])
    student_email = sys.argv[3]

    # Set up the interface
    top = tkinter.Tk()
    top.title("OMSI Online Help")

    entry_label = tkinter.Label(top, text="Question (Please make it clear and concise): ")
    response_label = tkinter.Label(top, text="Responses: ")
    entry_label.grid(row=0)
    response_label.grid(row=3)

    question_entry = tkinter.Text(top, font=("sans-serif", 12), bg="azure")
    question_entry.insert("end", "<Please entry your question here>")
    question_entry.grid(row=1)

    response_entry = tkinter.Text(top, font=("sans-serif", 12), bg="azure")
    response_entry.configure(state="disabled")
    response_entry.grid(row=4)

    # Callback for the button
    def send_message():
        response_entry.configure(state="normal")
        response_entry.insert("end", "Waiting for response...\n")
        response_entry.configure(state="disabled")
        send_button["state"] = "disabled"

        def actions_after_responses():
            header = student_email + " asked: \n"
            outbound_msg = header + question_entry.get("1.0", "end")
            msg_received = query(server_addr, port, outbound_msg)

            response_entry.configure(state="normal")
            response_entry.insert("end", msg_received+"\n")
            response_entry.configure(state="disabled")
            send_button["state"] = "normal"

        # Threading prevents the client from non-responding
        threading.Thread(target=actions_after_responses).start()

    send_button = tkinter.Button(text="Send", command=send_message)
    send_button.grid(row=2)

    # Set sail!
    top.mainloop()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 chat_client.py <server_addr> <port> <email_address>")
        sys.exit(1)
    gui_setup()
