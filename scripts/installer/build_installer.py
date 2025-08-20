import os
import sys
import subprocess

ISSC_PATH = os.path.expanduser(r"~\Desktop\Coding\InnoSetup\ISCC.exe")

script_dir = os.path.dirname(os.path.abspath(__file__))
DOT_ISS_PATH = os.path.join(script_dir, 'downly_installer.iss')

def build_installer():
        # Check if Inno Setup compiler was found
        if not ISSC_PATH:
                print("Error: Inno Setup compiler (ISCC.exe) not found.")
                print("Please install Inno Setup or set the correct path.")
                print("Common installation locations:")
                print("  - C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe")
                print("  - C:\\Program Files\\Inno Setup 6\\ISCC.exe")
                print("Or set environment variable: INNO_SETUP_PATH")
                return False
                
        if not os.path.exists(ISSC_PATH):
                print(f"Error: Inno Setup compiler not found at: {ISSC_PATH}")
                print("Please verify the path or install Inno Setup.")
                return False
        
        # Check if ISS file exists
        if not os.path.exists(DOT_ISS_PATH):
                print(f"Error: ISS file not found at: {DOT_ISS_PATH}")
                return False
        
        # Check if build_output directory exists
        project_root = os.path.dirname(os.path.dirname(script_dir))
        portable_path = os.path.join(project_root, 'build_output', 'portable', 'downly')
        if not os.path.exists(portable_path):
                print(f"Error: Built application not found at: {portable_path}")
                print("Please run the build script first to create the application.")
                return False
        
        # Create installer output directory if it doesn't exist
        installer_output_dir = os.path.join(project_root, 'build_output', 'installer')
        os.makedirs(installer_output_dir, exist_ok=True)
        
        # Define the command to run Inno Setup
        command = [
                ISSC_PATH,  # Path to Inno Setup Compiler                           
                DOT_ISS_PATH  # Path to the ISS file
        ]
        
        # Run the command
        print("Building Downly installer with Inno Setup...")
        try:
                result = subprocess.run(command, check=True)
                print("Installer build completed successfully.")
                return True
        except subprocess.CalledProcessError as e:
                print(f"Installer build failed with error: {e}")
                return False
        except FileNotFoundError as e:
                print(f"Inno Setup compiler not found at: {ISSC_PATH}")
                print("Please check the ISSC_PATH variable and ensure Inno Setup is installed.")
                return False

if __name__ == "__main__":
        success = build_installer()
        if not success:
                exit(1)