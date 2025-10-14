from flask import Flask, request, redirect, url_for


# Define the Flask app
app = Flask(__name__)

admins = {"admin" : "password"} 
subscribers = {"test" : "123"}
admin_message = None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username in subscribers and password == subscribers[username]:
            return redirect(url_for("welcome", username=username))
        elif username in admins and password == admins[username]:
            return redirect(url_for("admin_dashboard", username=username))
        elif  username in subscribers and password != subscribers[username] or username in admins and password != admins[username]:
            return '''
                <body style="background-color: #ffebee;">
                  <div style="text-align:center; margin-top: 10vh;">
                    <h2>Error: Incorrect password.</h2>
                    <a href="/sign_up">Sign up</a> | <a href="/">Return to Login</a>
                  </div>
                </body>
            ''', 400

        else:
            return '''
                <body style="background-color: #e0f7fa;">
                  <div style="text-align:center; margin-top: 10vh;">
                    <h2>Error: Invalid username or password.</h2>
                    <a href="/sign_up">Sign up</a> | <a href="/">Return to Login</a>
                  </div>
                </body>
            ''', 400
    return '''
        <body style="background-color: #e0f7fa;">
          <div style="text-align:center; margin-top: 10vh;">
            <h2>Login</h2>
            <form method="post">
                <label>Username: <input type="text" name="username"></label><br>
                <label>Password: <input type="password" name="password"></label><br>
                <input type="submit" value="Login">
            </form>
            <a href="/sign_up">Sign up</a>
          </div>
        </body>
    '''

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username in subscribers:
            return '''
                <body style="background-color: #ffebee;">
                  <div style="text-align:center; margin-top: 10vh;">
                    <h2>Error: Username already exists.</h2>
                    <a href="/sign_up">Try again</a> | <a href="/">Return to Login</a>
                  </div>
                </body>
            ''', 400
        elif username and password:
            subscribers[username] = password
            return redirect(url_for("welcome", username=username))
        else:
            return '''
                <body style="background-color: #fff3e0;">
                  <div style="text-align:center; margin-top: 10vh;">
                    <h2>Error: Please enter both username and password.</h2>
                    <a href="/sign_up">Try again</a> | <a href="/">Return to Login</a>
                  </div>
                </body>
            ''', 400
    return '''
        <body style="background-color: #fff3e0;">
          <div style="text-align:center; margin-top: 10vh;">
            <h2>Sign Up</h2>
            <form method="post">
                <label>Username: <input type="text" name="username"></label><br>
                <label>Password: <input type="password" name="password"></label><br>
                <input type="submit" value="Sign Up">
            </form>
            <a href="/">Return to Login</a>
          </div>
        </body>
    '''

@app.route('/welcome/<username>', methods=['GET', 'POST'])
def welcome(username):
    message = ""

    if request.method == 'POST':
        # Handle password change
        if 'new_password' in request.form:
            current_password = request.form.get('password', '')
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            if subscribers.get(username) != current_password:
                message = "❌ Error: Current password is incorrect.",
            elif new_password != confirm_password:
                message = "❌ Error: Passwords do not match.",
            else:
                subscribers[username] = new_password
                message = "✅ Password updated successfully!", 

        # Handle unsubscribe confirmation
        elif 'confirm_unsubscribe' in request.form:
            entered_password = request.form.get('password', '')

            if subscribers.get(username) != entered_password:
                message = "❌ Error: Incorrect password. Unsubscribe failed."
            else:
                del subscribers[username]
                return redirect(url_for('login'))
    global admin_message
    display_message = admin_message if admin_message else "No message from the admins yet."

    return f"""
        <body style="background-color: #e8f5e9; font-family: Arial, sans-serif;">
          <div style="text-align:center; margin-top: 5vh;">
            <h2>Welcome, {username}!</h2>

            <!-- Messages -->
            <div style="margin-top: 30px;">
              <h3>📨 Messages from Admins</h3>
              <div id="messages" 
                   style="border: 1px solid #ccc; border-radius: 8px; background: #fff; 
                          width: 60%; margin: 0 auto; padding: 10px; text-align:left;">
                <p>{display_message}</p>
              </div>
            </div>

            <!-- Change Password -->
            <div style="margin-top: 40px;">
              <h3>🔒 Account Settings</h3>
              <button onclick="togglePasswordForm()" 
                      style="padding: 8px 16px; border: none; background-color: #4CAF50; color: white; border-radius: 5px;">
                Change Password
              </button>

              <form id="passwordForm" method="POST" style="display:none; margin-top: 15px;">
                <input type="password" name="password" placeholder="Current password" required
                       style="padding: 8px; border-radius: 5px; border: 1px solid #ccc;">
                <input type="password" name="new_password" placeholder="New password" required
                       style="padding: 8px; border-radius: 5px; border: 1px solid #ccc; margin-left: 10px;">
                <input type="password" name="confirm_password" placeholder="Confirm new password" required
                       style="padding: 8px; border-radius: 5px; border: 1px solid #ccc; margin-left: 10px;">
                <button type="submit" style="padding: 8px 16px; border: none; background-color: #388e3c; color: white; border-radius: 5px;">
                  Update
                </button>
              </form>
            </div>

            <!-- Unsubscribe -->
            <div style="margin-top: 40px;">
              <button onclick="toggleUnsubscribeForm()" 
                      style="padding: 8px 16px; border: none; background-color: #e53935; color: white; border-radius: 5px;">
                Unsubscribe
              </button>

              <form id="unsubscribeForm" method="POST" style="display:none; margin-top: 15px;">
                <p style="color:#555;">Please confirm your password to unsubscribe:</p>
                <input type="password" name="password" placeholder="Enter your password" required
                       style="padding: 8px; border-radius: 5px; border: 1px solid #ccc;">
                <button type="submit" name="confirm_unsubscribe"
                        style="padding: 8px 16px; border: none; background-color: #b71c1c; color: white; border-radius: 5px; margin-left: 10px;">
                  Confirm Unsubscribe
                </button>
              </form>
            </div>

            <!-- Logout -->
            <div style="margin-top: 30px;">
              <a href="/" style="color: #2e7d32; text-decoration:none;">Logout</a>
            </div>

            <!-- Status Message -->
            <p style="color: #2e7d32; margin-top: 20px;">{message}</p>
          </div>

          <script>
            function togglePasswordForm() {{
                const form = document.getElementById('passwordForm');
                form.style.display = form.style.display === 'none' ? 'block' : 'none';
            }}
            function toggleUnsubscribeForm() {{
                const form = document.getElementById('unsubscribeForm');
                form.style.display = form.style.display === 'none' ? 'block' : 'none';
            }}
          </script>
        </body>
    """

@app.route('/admin/<username>', methods=['GET', 'POST'])
def admin_dashboard(username):
    message = ""
    if request.method == 'POST':
        if 'new_password' in request.form and 'new_username' in request.form:
            current_password = request.form.get('password', '')
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            new_username = request.form['new_username']


            if admins.get(username) != current_password:
                message = "❌ Error: Current password is incorrect."
            elif new_password != confirm_password:
                message = "❌ Error: Passwords do not match."
            elif new_username in admins:
                message = "❌ Error: Username already exists."
            else:
                admins[new_username] = new_password
                if new_username != username:
                    del admins[username]
                    message = "✅ Credentials updated successfully! Logout to re-login to complete changes."
    return f"""
    <body style="background-color:#f0f4f8; font-family:Arial,sans-serif; text-align:center; margin-top:5vh;">
      <h2>Welcome Admin {username}!</h2>
      
      <div style="margin-top:30px;">
        <a href="/admin/subscribers">
          <button style="padding:10px 20px; background-color:#4CAF50; color:white; border:none; border-radius:8px; margin:10px;">
            View Subscribers
          </button>
        </a>
        <a href="/admin/post_message">
          <button style="padding:10px 20px; background-color:#2196F3; color:white; border:none; border-radius:8px; margin:10px;">
            Post Message
          </button>
        </a>
      </div>

      <!-- Change Credentials -->
      <div style="margin-top: 40px;">
       <h3>🔒 Account Settings</h3>
        <button onclick="ChangeCredentials()" 
              style="padding: 8px 16px; border: none; background-color: #4CAF50; color: white; border-radius: 5px;">
                Change Credentials
        </button>

        <form id="ChangeCredentials" method="POST" style="display:none; margin-top: 15px;">
          <input type="text" name="new_username" placeholder="New username" required
                       style="padding: 8px; border-radius: 5px; border: 1px solid #ccc; margin-bottom:10px;">
          <input type="password" name="password" placeholder="Current password" required
                       style="padding: 8px; border-radius: 5px; border: 1px solid #ccc;">
          <input type="password" name="new_password" placeholder="New password" required
                       style="padding: 8px; border-radius: 5px; border: 1px solid #ccc; margin-left: 10px;">
          <input type="password" name="confirm_password" placeholder="Confirm new password" required
                       style="padding: 8px; border-radius: 5px; border: 1px solid #ccc; margin-left: 10px;">
          <button type="submit" style="padding: 8px 16px; border: none; background-color: #388e3c; color: white; border-radius: 5px;">
             Update
          </button>
          </form>
      </div>

      <!-- Logout -->
      <div style="margin-top: 30px;">
        <a href="/" style="color: #2e7d32; text-decoration:none;">Logout</a>
      </div>

           <!-- Status Message -->
            <p style="color: #2e7d32; margin-top: 20px;">{message}</p>
          </div>

          <script>
            function ChangeCredentials() {{
                const form = document.getElementById('ChangeCredentials');
                form.style.display = form.style.display === 'none' ? 'block' : 'none';
            }}
          </script>
        </body>
    """



@app.route('/admin/<username>/subscribers')
def view_subscribers(username):
    users_list = "<ul style='list-style:none; padding:0;'>"
    for user in subscribers.keys():
        users_list += f"""
          <li style='margin:10px;'>
            👤 {user}
            <a href='/admin/remove_user/{user}' style='margin-left:15px;'>
              <button style='padding:5px 10px; background-color:#e53935; color:white; border:none; border-radius:5px;'>
                Remove
              </button>
            </a>
          </li>
        """
    users_list += "</ul>"

    return f"""
    <body style="background-color:#fff8e1; font-family:Arial,sans-serif; text-align:center; margin-top:5vh;">
      <h2>👥 Current Subscribers</h2>
      {users_list}
      <div style="margin-top:30px;">
        <a href="/admin/{username}">
          <button style="padding:8px 16px; background-color:#616161; color:white; border:none; border-radius:5px;">
            Back to Dashboard
          </button>
        </a>
      </div>
    </body>
    """

# ---------- REMOVE A USER ----------
@app.route('/admin/<admin_username>/remove_user/<username>')
def remove_user(admin_username,username):
    if username in subscribers:
        del subscribers[username]
        msg = f"✅ User '{username}' removed successfully."
    else:
        msg = f"⚠️ User '{username}' not found."

    return f"""
    <body style="font-family:Arial,sans-serif; text-align:center; margin-top:5vh;">
      <h2>{msg}</h2>
      <a href="/admin/{admin_username}/subscribers">
        <button style="padding:8px 16px; background-color:#4CAF50; color:white; border:none; border-radius:5px;">
          Back to Subscribers
        </button>
      </a>
    </body>
    """


# ---------- POST MESSAGE ----------
@app.route('/admin/<username>/post_message', methods=['GET', 'POST'])
def post_message(username):
    message = ""

    if request.method == 'POST':
        global admin_message
        admin_message = request.form['message']
        message = f"✅ Message posted! All users notified ({len(subscribers)} total)."

    return f"""
    <body style="background-color:#e3f2fd; font-family:Arial,sans-serif; text-align:center; margin-top:5vh;">
      <h2>📝 Post a Message to All Users</h2>
      <form method="POST" style="margin-top:20px;">
        <textarea name="message" rows="4" cols="50" placeholder="Type your announcement here..." required
                  style="border-radius:8px; padding:10px; border:1px solid #ccc;"></textarea><br><br>
        <button type="submit" style="padding:8px 16px; background-color:#1976D2; color:white; border:none; border-radius:5px;">
          Post Message
        </button>
      </form>
      <p style="color:#2e7d32; margin-top:20px;">{message}</p>

      <div style="margin-top:30px;">
        <a href="/admin/{username}">
          <button style="padding:8px 16px; background-color:#616161; color:white; border:none; border-radius:5px;">
            Back to Dashboard
          </button>
        </a>
      </div>
    </body>
    """


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
