import os
import sys
import subprocess

# Update the path to the Inno Setup script
ISSC_PATH = r"C:\Users\Morgan\Desktop\Coding\InnoSetup\ISCC.exe"

script_dir = os.path.dirname(os.path.abspath(__file__))
DOT_ISS_PATH = os.path.join(script_dir, 'downly_installer.iss')

def build_installer():
        # Check if Inno Setup compiler exists
        if not os.path.exists(ISSC_PATH):
                print(f"Error: Inno Setup compiler not found at: {ISSC_PATH}")
                print("Please update the ISSC_PATH variable or install Inno Setup.")
                return False
        
        # Check if ISS file exists
        if not os.path.exists(DOT_ISS_PATH):
                print(f"Error: ISS file not found at: {DOT_ISS_PATH}")
                return False
        
        # Check if dist directory exists
        dist_path = os.path.join(os.path.dirname(script_dir), 'dist', 'downly')
        if not os.path.exists(dist_path):
                print(f"Error: Built application not found at: {dist_path}")
                print("Please run the build script first to create the application.")
                return False
        
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