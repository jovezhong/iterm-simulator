import iterm2
import asyncio
import re
import os
import pyparsing as pp
from markdown_it import MarkdownIt
import argparse

import pyautogui
import subprocess
from functools import partial


keyboard_shortcuts = {
    "Ctrl+A": '\x01',  # Move to the beginning of the line
    "Ctrl+B": '\x02',  # Move backward one character
    "Ctrl+C": '\x03',  # Interrupt (send SIGINT to) the current process
    "Ctrl+D": '\x04',  # Delete the character under the cursor (EOF if line is empty)
    "Ctrl+E": '\x05',  # Move to the end of the line
    "Ctrl+F": '\x06',  # Move forward one character
    "Ctrl+G": '\x07',  # Bell (beep)
    "Ctrl+H": '\x08',  # Backspace (same as the backspace key)
    "Ctrl+I": '\x09',  # Tab (same as the Tab key)
    "Ctrl+J": '\x0a',  # Newline (same as the Enter/Return key)
    "Ctrl+K": '\x0b',  # Kill (cut) text from the cursor to the end of the line
    "Ctrl+L": '\x0c',  # Clear the screen
    "Ctrl+M": '\x0d',  # Carriage return (same as the Enter/Return key)
    "Ctrl+N": '\x0e',  # Move to the next line in history
    "Ctrl+O": '\x0f',  # Execute the current line and fetch the next line from history
    "Ctrl+P": '\x10',  # Move to the previous line in history
    "Ctrl+Q": '\x11',  # Resume transmission (used with software flow control)
    "Ctrl+R": '\x12',  # Reverse search in history
    "Ctrl+S": '\x13',  # Suspend transmission (used with software flow control)
    "Ctrl+T": '\x14',  # Transpose (swap) the character under the cursor with the one before it
    "Ctrl+U": '\x15',  # Kill (cut) text from the cursor to the beginning of the line
    "Ctrl+V": '\x16',  # Quoted insert (insert the next character verbatim)
    "Ctrl+W": '\x17',  # Kill (cut) the word before the cursor
    "Ctrl+X": '\x18',  # Used as a prefix for other shortcuts
    "Ctrl+Y": '\x19',  # Yank (paste) the most recently killed text
    "Ctrl+Z": '\x1a',   # Suspend the current process (send SIGTSTP)

    "ArrowUp": '\x1b[A',
    "ArrowDown": '\x1b[B',  # Updated based on the output from tput
    "ArrowRight": '\x1b[C',
    "ArrowLeft": '\x1b[D',

    'Enter': '\n',
    "Space": '\x20',
    'Delete': '\x7f',
    'Backspace': '\x08',
    'Escape': '\x1b',
}

def move(direction, modifier):
    pyautogui.keyDown(modifier)
    pyautogui.press(direction)
    pyautogui.keyUp(modifier)

pyautogui_shortcuts = {
    "ScrollUpOneLine": partial(move, 'up', 'command'),
    "ScrollDownOneLine": partial(move, 'down', 'command')
}

valid_prompts = [
    "$",
    ">>>",
    ">>> Send a message (/? for help)",
    "...",
    '⚫◗',
    'MN :)',
    ':)',
    '"Modelfile" [New]',
    '-- INSERT --'
] + [f"In [{id}]:" for id in range(0,1000)]

def activate_iterm():
    script = """
        tell application "iTerm"
            activate
        end tell
    """
    os.system(f"osascript -e '{script}'")

# # Then call this function at the appropriate place in your script
# activate_iterm()



async def wait_for_prompt(session):
    await asyncio.sleep(0.5)  # short delay

    while True:
        # Get the session's screen contents
        screen_contents = await session.async_get_screen_contents()

        # Determine the number of lines
        num_lines = screen_contents.number_of_lines

        # Extract the lines from the screen contents
        lines_data = [screen_contents.line(i) for i in range(num_lines)]

        # Find the last non-empty line
        for line_data in reversed(lines_data):
            last_line = line_data.string.strip()
            if last_line:
                break

        print(f"Detected last line: [{last_line.strip()}]")

        if last_line.strip() in valid_prompts:
            print("Command finished")
            break
        await asyncio.sleep(0.1)


in_less = False

# async def simulated_typing(session, text, delay=0.1, press_enter=True):
#     global in_less
#     print(delay)

#     if "less" in text.strip():
#         in_less = True

#     if in_less:
#         for char in text:
#             await session.async_send_text(char)
#             await asyncio.sleep(delay)
#         if press_enter:
#             await session.async_send_text("\n")
#         await asyncio.sleep(0.1)  # A short sleep just to simulate the immediate execution in less
#     else:
#         for char in text:
#             await session.async_send_text(char)
#             await asyncio.sleep(delay)
#         if press_enter:
#             print(f"Press enter [{press_enter}]")
#             await session.async_send_text("\n")
#             await wait_for_prompt(session)

#     # Check if it's a command to exit from less (typically "q")
#     if text.strip() == "q":
#         in_less = False

async def simulated_typing(session, command, delay=0.1):
    global in_less
    print(delay)

    text = command.text()
    press_enter = command.press_enter
    wait = command.wait_for_prompt    

    if "less" in text.strip():
        in_less = True

    if in_less:
        for char in text:
            await session.async_send_text(char)
            await asyncio.sleep(delay)
        if press_enter:
            await session.async_send_text("\n")
        await asyncio.sleep(0.1)  # A short sleep just to simulate the immediate execution in less
    else:
        for char in text:
            await session.async_send_text(char)
            await asyncio.sleep(delay)
        if press_enter:
            print(f"Press enter [{press_enter}], Wait [{wait}], Command [{command}]")
            await session.async_send_text("\n")
            if wait:
                await wait_for_prompt(session)
            else: 
                await asyncio.sleep(0.1)

    # Check if it's a command to exit from less (typically "q")
    if text.strip() == "q":
        in_less = False


async def find_or_create_session(app, window_index=None, tab_index=None):
    windows = app.windows
    if window_index is not None and 0 <= window_index < len(windows):
        window = windows[window_index]
    else:
        window = app.current_window
        if not window:
            window = await iterm2.Window.async_create(connection)

    # Activate the window
    await window.async_activate()

    tabs = window.tabs
    if tab_index is not None and 0 <= tab_index < len(tabs):
        tab = tabs[tab_index]
    else:
        tab = window.current_tab
        if not tab:
            tab = await window.async_create_tab()

    # Activate the tab
    await tab.async_activate()

    session = tab.current_session
    if not session:
        session = await tab.async_create_session()

    return session


# Define grammar for a keyboard shortcut using pyparsing
LBRACK = pp.Literal("[")
RBRACK = pp.Literal("]")
ASTERISK = pp.Literal("*")
MULTIPLIER = pp.Word(pp.nums).setParseAction(lambda t: int(t[0]))
FLOAT = pp.Combine(pp.Word(pp.nums) + pp.Optional(pp.Literal(".") + pp.Word(pp.nums))).setParseAction(lambda t: float(t[0]))
KEYWORD = pp.Word(pp.alphas + "+")

SLEEP_TIME = pp.Suppress(pp.Literal("sleep=")) + FLOAT

keyboard_command = (LBRACK + KEYWORD("keyword") + 
                    pp.Optional(ASTERISK + MULTIPLIER("multiplier") + 
                                SLEEP_TIME("sleep_time")) + 
                    RBRACK)

EQUALS = pp.Literal("=")
ATTRIBUTE_NAME = pp.Word(pp.alphas)
ATTRIBUTE_VALUE = FLOAT | pp.Keyword("true") | pp.Keyword("false")
ATTRIBUTE = ATTRIBUTE_NAME("name") + pp.Suppress(EQUALS) + ATTRIBUTE_VALUE("value")
ALL_ATTRIBUTES = pp.OneOrMore(ATTRIBUTE)

def extract_attributes_from_info(info_string):
    attributes = {}
    matches = ALL_ATTRIBUTES.searchString(info_string)
    if len(matches) > 0:
        matching = matches[0]
        for i in range(0, len(matching), 2):
            attributes[matching[i]] = matching[i+1]
    return attributes


def extract_commands_from_md(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return extract_commands_from_text(content)

from dataclasses import dataclass, astuple

@dataclass
class Command:
    """A terminal command"""
    item:str
    sleep_before: float = 0.0
    sleep_after: float = 1.0
    press_enter: bool = True
    strip: bool = True
    wait_for_prompt: bool = False

    def text(self) -> str:
        if self.strip:
            return self.item.strip()
        else:
            return self.item.rstrip("\n")


def extract_commands_from_text(content):
    md = MarkdownIt()
    tokens = md.parse(content)
    items = []

    for token in tokens:
        if token.type == "fence" and token.tag == "code":
            print("token.info", token.info)
            attributes = extract_attributes_from_info(token.info)
            print("attributes", attributes)

            sleep_before = float(attributes.get("sleepBefore", 0))
            sleep_after = float(attributes.get("sleep", 1))
            send_enter = attributes.get("enter", "true") == "true"
            strip_whitespace = attributes.get("strip", "true") == "true"
            wait_prompt = attributes.get("wait", "true") == "true"
            
            command = Command(token.content, sleep_before, sleep_after, send_enter, strip_whitespace, wait_for_prompt=wait_prompt)
            print("send_enter", send_enter, "wait_prompt", wait_prompt, "token.content", token.content, "Command", command)
            items.append(command)

        elif token.type == "inline":
            try:
                match = keyboard_command.parseString(token.content, parseAll=True)
                keyword = match["keyword"]
                mul = match.get("multiplier", 1)
                sleep = match["sleep_time"][0] if "sleep_time" in match else 1
                print("Token:", token.content, "Keyword: ", keyword, "Mul:", mul, "Sleep:", sleep, "Match:", match)
                for _ in range(mul):
                    items.append(Command(item = keyword, sleep_after=sleep))
            except pp.ParseException:
                print("No match for:" + token.content)
                pass  # Not a recognized keyboard command


    return items



async def main(connection, args):
    print(args)
    activate_iterm()
    app = await iterm2.async_get_app(connection)
    
    # Find or create the specific window, tab, and session
    window_index = args.window
    tab_index = args.tab
    session = await find_or_create_session(app, window_index=window_index, tab_index=tab_index)

    commands = extract_commands_from_md(args.filename)
    for command in commands:
        item, sleep_before, sleep_after, press_enter, strip, wait_for_prompt = astuple(command)
        print("item:", item, sleep_after, press_enter, keyboard_shortcuts.get(item))
        if item in keyboard_shortcuts:
            print(f"Send keyboard command for {item} -> {keyboard_shortcuts[item]}")
            await session.async_send_text(keyboard_shortcuts[item])
            await asyncio.sleep(sleep_after or 0.1)
        else:
            if item in pyautogui_shortcuts:
                pyautogui_shortcuts[item]()
                await asyncio.sleep(sleep_after or 0.1)

            else:
                await asyncio.sleep(sleep_before or 0)
                # await simulated_typing(session, command.text(), press_enter=press_enter, delay=args.delay)
                await simulated_typing(session, command = command, delay=args.delay)
                print("Sleep", sleep_after)
                await asyncio.sleep(sleep_after or 1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--filename', metavar='v', type=str)
    parser.add_argument('--window', metavar='v', type=int, default=0)
    parser.add_argument('--tab', metavar='v', type=int, default=0)
    parser.add_argument('--delay', metavar='v', type=float, default=0.1)
    args = parser.parse_args()

    iterm2.run_until_complete(lambda conn: main(conn, args))

