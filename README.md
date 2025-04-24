# chat-app-CN
A Python-based real-time chat application using socket programming. It features a server-client model, user authentication, and a simple Tkinter GUI for messaging between multiple users.


Based on the files you provided, here is a suitable description to add to your GitHub repository for the **Computer Network course chatting app**:

---

**Project Description**

This project is a Python-based **Computer Network Chatting Application** that allows real-time communication between users over a network using **socket programming**. The app consists of a server-client architecture where the server manages multiple client connections, enabling users to chat with each other in a secure environment.

### Features:
- **Real-time Messaging**: Users can send and receive messages instantly using socket-based communication.
- **Multiple Chat Rooms**: Users can communicate in a general chat room or directly with specific users.
- **User Authentication**: Users are required to sign in or sign up to access the chat functionality.
- **Server Management**: The server is capable of handling multiple client connections simultaneously, ensuring that messages are routed correctly.
- **User Interface**: A simple graphical user interface (GUI) is built using **Tkinter**, providing an intuitive platform for users to send messages, join rooms, and manage their connections.

### Technologies Used:
- **Python**: The application is developed using Python 3.x.
- **Socket Programming**: For creating a server-client communication channel.
- **Tkinter**: For the graphical user interface to manage chats and display messages.
- **Threading**: To handle multiple clients and ensure real-time communication without delays.

### Installation Instructions:
1. Clone this repository to your local machine.
   ```
   git clone   https://github.com/kedar49/Chat_CN.git
   ```
2. Navigate to the project directory and install any dependencies (if any).
   ```
   cd Chat_CN
   ```
3. Run the server using the command:
   ```
   python main.py
   ```
4. Start the client application by running the following command:
   ```
   python client.py
   ```

### How to Use:
- Launch the server first, then open multiple client windows to simulate user connections.
- Sign in with your credentials or create a new account.
- Chat with others by selecting usernames or use the broadcast feature to send messages to everyone in the chat room.

---

