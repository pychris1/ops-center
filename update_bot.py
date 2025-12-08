import os
import subprocess
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# --- CONFIGURATION ---
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)

@app.message("check updates")
def check_updates(message, say):
    say(f"Checking Ubuntu for updates... please wait.")
    
    try:
        result = subprocess.run(
            ['/usr/lib/update-notifier/apt-check', '--human-readable'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        # apt-check sometimes outputs to stderr, sometimes stdout. We combine them.
        output = (result.stdout + result.stderr).strip()

        # --- SMART LOGIC FIX ---
        # Check for the number 0 in the "immediately" line
        if "0 updates can be applied" in output or "0 packages can be updated" in output:
            say("*Good news!* No updates found. Your system is fully patched.")
        else:
            # If genuine updates exist, show them (but filter out the ESM spam if possible)
            say(f"*Updates Available:*\n{output}\n\nTo install, log in and run: `sudo apt upgrade`")

    except Exception as e:
        say(f"Error executing update check: {str(e)}")

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
