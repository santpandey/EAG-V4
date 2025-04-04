# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
import pywinauto
from pywinauto.application import Application
import win32gui
import win32con
import time
from win32api import GetSystemMetrics

# instantiate an MCP server client
mcp = FastMCP("Calculator")

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]


@mcp.tool()
async def draw_rectangle(x1: int, y1: int, x2: int, y2: int) -> dict:
    """Draw a rectangle in Paint from (x1,y1) to (x2,y2)"""
    global paint_app
    try:
        if not paint_app:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paint is not open. Please call open_paint first."
                    )
                ]
            }
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Get primary monitor width to adjust coordinates
        #primary_width = GetSystemMetrics(0)
        
        # Ensure Paint window is active
        if not paint_window.has_focus():
            paint_window.set_focus()
            time.sleep(0.2)
        
        # Click on the Rectangle tool using the correct coordinates for secondary screen
        #paint_window.click_input(coords=(513, 130 ))
        paint_window.type_keys("+t")
        time.sleep(0.2)
        #pywinauto.mouse.move_mouse_input(coords=(0, 400))
        #time.sleep(0.5)
        
        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        canvas.set_focus()
        canvas.type_keys("+t")
        time.sleep(0.2)
        # Draw rectangle - coordinates should already be relative to the Paint window
        # No need to add primary_width since we're clicking within the Paint window
        #canvas.press_mouse_input(coords=(x1+100, y1))
        canvas.press_mouse_input(coords=(x1, y1))
        #canvas.move_mouse_input(coords=(x2+100, y2))
        #canvas.move_mouse_input(coords=(x2+100, y2))
        #canvas.move_mouse_input(coords=(x2+100, y2))
        #canvas.move_mouse_input(coords=(x2+100, y2))
        canvas.drag_mouse_input(dst=(x2, y1), src=(x1, y1))
        canvas.drag_mouse_input(dst=(x2, y2), src=(x2, y1))
        canvas.drag_mouse_input(dst=(x1, y2), src=(x2, y2))
        canvas.drag_mouse_input(dst=(x1, y1), src=(x1, y2))
        #canvas.release_mouse_input(coords=(x2+100, y2))
        canvas.release_mouse_input(coords=(x1, y1))

        #canvas.press_mouse_input(coords=(x1+100, y1))
        #canvas.drag_input(dst=(x2+100, y2))
        #canvas.release_mouse_input(coords=(x2+100, y2))
        #paint_window.type_keys("+t")
        # Draw a rectangle
        #canvas.press_mouse_input(coords=(576, 463))
        #canvas.move_mouse_input(coords=(781, 609))
        #canvas.release_mouse_input(coords=(781, 609))
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Rectangle drawn from ({x1},{y1}) to ({x2},{y2})",
                    canvas=canvas
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing rectangle: {str(e)}"
                )
            ]
        }
               
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing rectangle: {str(e)}"
                )
            ]
        }
        
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing rectangle: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def add_text_in_paint(text: str) -> dict:
    """Add text in Paint"""
    global paint_app
    try:
        if not paint_app:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paint is not open. Please call open_paint first."
                    )
                ]
            }
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Ensure Paint window is active
        if not paint_window.has_focus():
            paint_window.set_focus()
            time.sleep(0.5)
        
        

        # Click on the Rectangle tool
        #paint_window.click_input(coords=(798, 515))
        #time.sleep(0.5)
        
        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        
        # Select text tool using keyboard shortcuts
        paint_window.type_keys('t')
        time.sleep(0.5)
        paint_window.type_keys('x')
        time.sleep(0.5)
        
        # Click where to start typing
        canvas.click_input(coords=(798, 517))
        time.sleep(0.5)
        
        # Type the text passed from client
        paint_window.type_keys(text)
        time.sleep(0.5)
        
        # Click to exit text mode
        canvas.click_input(coords=(1050, 800))
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Text:'{text}' added successfully"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def open_paint() -> dict:
    """Open Microsoft Paint"""
    global paint_app
    try:
        paint_app = Application().start('mspaint.exe')
        time.sleep(2)
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        #time.sleep(1)
        #paint_window.type_keys("%f")
        #time.sleep(2)
        #paint_window.type_keys("^e")
        #time.sleep(3)
        #properties_dialogue = paint_window.child_window(title='Image Properties', control_type='Window')
        #properties_dialogue.wait('ready', timeout=10)
        
        #if properties_dialogue.exists():
        #    image_size_group = properties_dialogue.child_window(title='Image size', control_type='Group')
        #    width_edit = image_size_group.child_window(title='Width:', control_type='Edit')
        #    height_edit = image_size_group.child_window(title='Height:', control_type='Edit')
        #    width_edit.set_focus()
        #    width_edit.type_keys("{TAB}")
        #    height_edit.set_focus()
        #    height_edit.type_keys("{TAB}")

        #if properties_dialogue.exists():
        #    properties_dialogue.set_focus()
        #    properties_dialogue.type_keys("{TAB}")
        #    time.sleep(1)
        #    properties_dialogue.type_keys("{TAB}")
        #    time.sleep(1)
        #    properties_dialogue.type_keys("{ENTER}")
        #    time.sleep(1)
        #if properties_dialogue.exists():
        #    ok_button = properties_dialogue.child_window(title='OK', control_type='Button')
        #    if ok_button.exists():
        #        ok_button.click()
        #        time.sleep(1)
        
            
        #if properties_dialogue.exists():
        #    cancel_button = properties_dialogue.child_window(title='Cancel', control_type='Button')
        #    if cancel_button.exists():
        #        cancel_button.click()
        #        time.sleep(1)

        #if properties_dialogue.exists():
        #    close_button = properties_dialogue.child_window(title='Close', control_type='Button')
        #    if close_button.exists():
        #        close_button.click()
        #        time.sleep(1)
        #if properties_dialogue.exists():
        #    win32gui.PostMessage(paint_window.handle, win32con.WM_CLOSE, 0, 0)                

        #time.sleep(5)
        #if properties_dialog.exists():
        #    properties_dialog.type_keys("{ESC}")
        #    time.sleep(0.5)
        #    properties_dialog.type_keys("{ESC}")
        # Find the width and height edit controls within the "Image Size" group.
        # This part is more robust because it finds the controls relative to the group.

        #image_size_group = properties_dialog.child_window(title="Image size", control_type="Group")
        #width_edit = image_size_group.child_window(title="Width:", control_type="Edit")
        #height_edit = image_size_group.child_window(title="Height:", control_type="Edit")

        #width = width_edit.get_value()
        #height = height_edit.get_value()

        #print(f"Image Width: {width}")
        #print(f"Image Height: {height}")

        #properties_dialog.type_keys("%{F4}")
        
        #paint_window.set_focus()
        #time.sleep(1)

        #properties_dialog = paint_window.by(name='Image properties', control_type='Window').click()
        # Get primary monitor width
        #primary_width = GetSystemMetrics(0)

        # Click on the File tab
        #paint_window.child_window(title="File", control_type="TabItem").click()

        # Click on Image Properties
        #paint_window.child_window(title="Properties", control_type="MenuItem").invoke()

        # Wait for the Properties dialog to appear
        #properties_dialog = paint_window.child_window(title="Image properties", control_type="Window")

        # Extract data from the dialog
        #width_edit = properties_dialog.child_window(title="Width:", control_type="Edit")
        #height_edit = properties_dialog.child_window(title="Height:", control_type="Edit")
        #units_combo = properties_dialog.child_window(title="Units:", control_type="ComboBox")

        #width = width_edit.get_value()  # Get width value
        #height = height_edit.get_value()  # Get height value
        #units = units_combo.get_value()  # Get selected units (e.g., pixels, inches)

        #print(f"Width: {width}, Height: {height}")


        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        time.sleep(1)
        #width = canvas.rectangle().width()
        #height = canvas.rectangle().height()
    
        # First move to secondary monitor without specifying size
        #win32gui.SetWindowPos(
            #paint_window.handle,
            #win32con.HWND_TOP,
            #primary_width + 1, 0,  # Position it on secondary monitor
            #0, 0,  # Let Windows handle the size
            #win32con.SWP_NOSIZE  # Don't change the size
        #)
        
        # Now maximize the window
        win32gui.ShowWindow(paint_window.handle, win32con.SW_MAXIMIZE)
        time.sleep(0.2)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Paint opened successfully on secondary monitor and maximized",
                    canvas=canvas,
                    width=1200,
                    height=720
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Paint: {str(e)}"
                )
            ]
        }
# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")

@mcp.tool()
def extract_coordinates(data: list) -> list[int]:
    """Extracts height and width from the list"""

    try:
        #start_width_index = data.find("width=") + len("width=")
        #end_width_index = data.find(",", start_width_index)
        width = int(data[1])

        #start_height_index = data.find("height=") + len("height=")
        #end_height_index = data.find(")]}", start_height_index)
        height = int(data[0])

        # Calculate coordinates for the rectangle
        # Target area: 40-50% of the canvas
        target_area_min_ratio = 0.4
        target_area_max_ratio = 0.5

        # Calculate approximate side lengths for the rectangle, aiming for the middle.
        rect_width = int(width * 0.63)  # Adjusted factor to achieve ~45% area
        rect_height = int(height * 0.71)  # Adjusted factor to achieve ~45% area

        # Ensure rectangle dimensions don't exceed canvas
        rect_width = min(rect_width, width)
        rect_height = min(rect_height, height)

        #x1 = (width - rect_width)   # Center horizontally
        #y1 = (height - rect_height)
        x1 = width
        y1 = height/3  # Center vertically
        #x2 = x1 + rect_width
        x2 = x1+300
        y2 = y1+300
        #y2 = y1 + rect_height
        result = [x1, y1, x2, y2]
        return result

    except (ValueError, AttributeError, TypeError) as e:
        print(f"Error extracting height and width: {e}")
        return None

    



@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]


if len(sys.argv) > 1 and sys.argv[1] == "dev":
    print("RUNNING IN DEV MODE")
    mcp.run()  # Run without transport for dev server
else:
    print("RUNNING IN PRODUCTION MODE")
    mcp.run(transport="stdio")  # Run with stdio for direct execution
