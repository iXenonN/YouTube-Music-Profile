<h1 align="center" id="title">YouTube Music Github Profile</h1>

<p id="description">This project displays the song you are currently listening to on YouTube Music in real-time on your GitHub profile.</p>

<p align="center"><img src="https://img.shields.io/badge/Currently-Working-brightgreen" alt="shields">  <img src="https://img.shields.io/badge/Version-1.2-blue" alt="shields"> <img alt="Chrome Web Store Rating" src="https://img.shields.io/chrome-web-store/rating/bimommhpekpddlbmaaljdkcgcfclpkfo?label=Extension%20Rating">
 <img alt="GitHub Downloads (all assets, all releases)" src="https://img.shields.io/github/downloads/iXenonN/YouTube-Music-Profile/total?label=Project%20Downloads">
 <img alt="Static Badge" src="https://img.shields.io/badge/Last_Update-11%2F27%2F24-white">
</p



## Inspired From:
  - • kittinan [![GitHub](https://img.shields.io/badge/GitHub-black?style=flat&logo=GitHub)](https://github.com/kittinan) 
  - • natemoo-re [![GitHub](https://img.shields.io/badge/GitHub-black?style=flat&logo=GitHub)](https://github.com/natemoo-re) 
  - • Thanks to sigma67 [![GitHub](https://img.shields.io/badge/GitHub-black?style=flat&logo=GitHub)](https://github.com/sigma67)  for creating the unoffical YouTube Music api.

## 🔒 Privacy Policy

This project respects your privacy. **No personal data is collected, stored, or shared** at any time while using this project.

### What This Means:
- The project **does not collect** any user data.
- The project **does not store** any data locally or remotely.
- The project **does not share** any information with third parties.

This ensures that your privacy is fully protected while using this project.

If you have any questions or concerns regarding privacy, feel free to reach out via the contact information provided in this repository.
 
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   The project continuously monitors and displays the song you're currently listening to on YouTube Music directly on your GitHub profile. It updates in real-time ensuring your profile always shows the latest track.
*   When YouTube Music is not running or the application is offline the project gracefully switches to a default message or image indicating that no song is currently being played.
*   As an open-source project it encourages community contributions allowing users to suggest features report bugs or even develop plugins to extend its functionality.

<h2>🛠️ Installation Steps:</h2>

1. **Clonning Project**

    - Clone the project.
  
    ```
    git clone https://github.com/iXenonN/YouTube-Music-Profile.git
    ```
  
    - Find the cloned project file in local.
  
    ```
    cd YouTube-Music-Profile
    ```
2. **Installing libraries and requirements**

    - Open app.py with your favorite Python IDE.
    
    - Install the YouTube Music api. (thanks to sigma67 for creating this api)
    
    ```
    pip install ytmusicapi
    ```
    
    - In the cloned file install requirements.txt.
    ```
    pip install -r requirements.txt
    ```
    
3. **Editing ytmusicapi credentials and Generate browser.json for ytmusicapi. ("oauth-based authentication has been disabled for the web client by Google")**

   - Open a new tab from your browser. (Firefox recommended)
     
   - Open the developer tools (Ctrl-Shift-I) and select the “Network” tab.
     
   - Go to https://music.youtube.com and ensure you are logged in.
     
   - Find an authenticated POST request. The simplest way is to filter by '/browse' using the search bar of the developer tools. If you don’t see the request, try scrolling down a bit or clicking on the library button in the top bar.
  
   - For Firefox verify that the request looks like this: Status 200, Method POST, Domain music.youtube.com, File  ``` browse?...  ```
     - Copy the request headers. (right click > copy > copy request headers)
    
   - For Chromium (Chrome/Edge) verify that the request looks like this: Status 200, Name  ``` browse?... ```
     - Click on the Name of any matching request. In the “Headers” tab, scroll to the section “Request headers” and copy everything starting from “accept: */*” to the end of the section.

   - Then, open a console do  ```cd Desktop``` and call.
    ```
    ytmusicapi browser
    ```
   - Paste the request headers that you copied before to the terminal input and click theese keys respectively.
   ```
   Enter, Ctrl+Z, Enter
   ```
   - This command will create a browser.json file in your Desktop.
    
   - In the code change the 'YOUR BROWSER.JSON FILE' with your browser.json file.
    
    ```
    ytmusic = YTMusic('YOUR BROWSER.JSON FILE')
    ```

3. **Firebase Project**

     - Create a new project in Firebase.
    
     - Download your project's Firebase Admin SDK as node.js.
    
     - Copy your Firebase project url.

4. **Editing Code With Firebase Credentials**

    - Change the 'YOUR FIREBASE CRED JSON FILE' with your firebase admin sdk json file.
    
    ```
    cred = credentials.Certificate('YOUR FIREBASE CRED JSON FILE')
    ```
    
    - Paste your firebase project url to the 'YOUR FIREBASE PROJECT URL'.
    
    ```
    firebase_admin.initialize_app(cred {
        'storageBucket': 'YOUR FIREBASE PROJECT URL'
    })
    ```
    
    - Save and exit app.py.

5. **Chrome Extension**

    - Install the "YouTube Music Status Checker" chrome extension for checking the YouTube Music background status.
  
    ```
    https://chromewebstore.google.com/detail/youtube-music-status-chec/bimommhpekpddlbmaaljdkcgcfclpkfo?hl=tr
    ```

6. **GitHub README.md modify**

    - Open your profile readme.md by creating a repository with your GitHub username if you dont have already.
    
    - Go to your Firebase project.
    
    - Click the Storage tab.
    
    - Click on listening-on-ytmusic.svg file and click name then copy the url to your svg file.
    
    - Paste the text below to your profile's readme.md file and save:
  
    ```
      #
      ![What Am I Listening](your-copied-images-url)
    ```

7. **Creating the token for update-readme.yaml file**

    - Go to your GitHub settings.
    
    - Scroll and click Developer Settings.
    
    - Click Personal Acces Tokens and choose Tokens(classic).
    
    - Create a token gave acces to all and name whatever you want.
    
    - Copy your token.
  
    - **NEVER SHARE YOUR TOKEN.**
  
    - Go to settings in your profile's repository where readme.md file located.
    
    - Click secrets and variables.
    
    - Go to Actions tab.
    
    - Create a new repository secret name anything you want.
    
    - Paste your token to your repository secret you created.
    
    - Save and its all done now.

8. **Automate with GitHub Actions**

    - After you complete editing your readme.md file save it and go to your profile's repository.
    
    - Create a new file named update-readme.yaml into your .github/workflows folder.
    
    - Paste the code below:
    
    ```
    name: Update SVG Version
    
    on:
      push:
        branches:
          - main
      schedule:
        - cron: '*/2 * * * *'  # Runs every 2 minutes
      workflow_dispatch:
      
    jobs:
      update-version:
        runs-on: ubuntu-latest
        steps:
        - name: Checkout Repository
          uses: actions/checkout@v2
    
          
    
        - name: Increment SVG Version
          id: increment_version
          run: |
            current_version=$(grep -oP '(?<=v=)\d+' README.md)
            echo "Current version: $current_version"
            new_version=$((current_version + 1))
            echo "New version: $new_version"
            sed -i "s/v=$current_version/v=$new_version/" README.md
        
    
        - name: Commit Changes
          run: |
            git config --local user.email "YOUR GITHUB EMAIL"
            git config --local user.name "YOUR REPOSITORY ADMIN USERNAME"
            git add README.md
            git commit -m "Increment SVG version to v${{ steps.increment_version.outputs.new_version }}"
    
        - name: Push Changes
          uses: ad-m/github-push-action@v0.6.0
          with:
            github_token: ${{ secrets.YOUR_GITHUB_TOKEN_SECRET_NAME }}
            branch: main
    ```

9. **Run the code**

    - Double click on app.py.
    
    - If you have completed all these steps successfully the code should work.
  

<h2>🍰 Contribution Guidelines:</h2>

Thank you for considering contributing to this project! To ensure a smooth and effective collaboration, please follow these guidelines:

## How to Contribute

1. **Fork the Repository**
   - Click the "Fork" button at the top right of this repository to create a copy of the repository under your GitHub account.

2. **Clone the Repository**
   - Clone your forked repository to your local machine:
     ```bash
     git clone https://github.com/iXenonN/YouTube-Music-Profile.git
     ```

3. **Create a Branch**
   - Create a new branch for your feature or bug fix:
     ```bash
     git checkout -b feature/your-feature-name
     ```

4. **Make Your Changes**
   - Implement your feature or fix the bug. Please make sure your code follows the coding standards mentioned below.

5. **Commit Your Changes**
   - Write clear and concise commit messages:
     ```bash
     git commit -m "Add feature: your feature description"
     ```

6. **Push to Your Fork**
   - Push your changes to your forked repository:
     ```bash
     git push origin feature/your-feature-name
     ```

7. **Create a Pull Request**
   - Go to the original repository and create a pull request from your branch. Include a detailed description of your changes and the reason for the contribution.

## Coding Standards

- **Code Style:** Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- **Comments:** Write comments where necessary to explain the code, especially in complex logic.
- **Testing:** Ensure that your code passes all existing tests and add new tests if applicable.

## Issue Reporting

- **Search First:** Before submitting a new issue, please search the existing issues to avoid duplicates.
- **Detailed Reports:** When reporting a bug, include as much detail as possible (e.g., steps to reproduce, screenshots, and any error messages).

## Pull Request Process

- **Review:** All pull requests will be reviewed by the repository maintainers.
- **Feedback:** If changes are requested, please address them promptly and update the pull request.

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (e.g., MIT License).

---

Thank you for contributing! Your help is appreciated.

## 🚧 Troubleshooting & Common Issues

### ❌ Issue: `ModuleNotFoundError: No module named 'some_module'`
  - **Cause:** This error occurs when the required Python package is not installed.
  
  - **Solution:** Ensure that all dependencies are installed correctly by running:
  
  ```
  pip install -r requirements.txt
  
  ```

### ❌ Issue: `FileNotFoundError: [Errno 2] No such file or directory: 'browser.json'`
  - **Cause:** This error occurs when the project cannot find the browser.json file in the expected directory (It can be ).
  
  - **Solution:** Make sure that browser.json exists in the project's root directory. If it's missing, you can create with the command below (This error may also apply to your firebase-sdk.json. If you see this error message, it is useful       to check your firebase-sdk.json path as well.):
      ```
      ytmusicapi browser
      ```

### ❌ Issue: `'ytmusicapi' is not recognized as an internal or external command, operable program or batch file.`
  - **Cause:** This error occurs when your system cant see the ytmusicapi library (i think).
  
   - **1. Solution:** Add youtubemusicapi into your computers PATH as a enviromental variable. it should be in the
     ```
     C:\Users\{Your Username}\AppData\Roaming\Python\Python312\Scripts\ytmusicapi.exe
     ```
  
  - **2. Solution:** For me i use windows 11 and i had this issue too but luckily i had a linux installed virtual machine and i executed this command from linux and it worked, so you can try a diffrent operating system and transfer the browser.json file into your main operating system.


### ❌ Issue: `google.api_core.exceptions.NotFound: 404 POST [LINK]`
  - **Cause:** This error occurs when your firebase_admin.initialize_app(cred{'storageBucket': '' }) url is wrong.
  
  - **Solution:** Check your firebase project url again and make sure its the right url it should look like this:
      ```
      your-project-name.appspot.com
      ```
    
### ❌ Issue: `TimeoutError: [Errno 110] Connection timed out`
  - **Cause:** This error occurs when a network request takes too long to complete, often due to poor network connectivity or an unresponsive server.
  
  - **Solution:** Check your network connection and ensure that the server you are trying to reach is online. You may also increase the timeout limit in your request:
      ```
          response = requests.get(image_url, timeout=10)
      ```
      and:
      ```
          response = requests.get(thumbnail_url, timeout=10)
      ```
    
### ❌ Issue: `CORS policy: No 'Access-Control-Allow-Origin' header is present.`
  - **Cause:** This error occurs when your Flask server does not allow cross-origin requests.
  
  - **Solution:** Ensure that flask-cors is installed and properly configured in your Flask application. You can add the following lines to your app.py:
      ```
          from flask_cors import CORS
          app = Flask(__name__)
          CORS(app)
      ```

### ❌ Issue: `UI not changing`
  - **Cause:** i really dont know why this happens but i think GitHub's 5k rate limit causes this.
  
  - **Solution:** Just go to the actions tab in your profile's repository and then run the update-readme.yaml that will fix the issue and sometimes ctrl + f5 solves too.


## 📧 Still Having Issues?
  - If you're still experiencing issues after trying these solutions, feel free to open an issue or contact me directly via email. ![Gmail](https://img.shields.io/badge/alikeremergen13%40gmail.com-grey?logo=Gmail) & ![GmailAlternative](https://img.shields.io/badge/chocolate45012%40gmail.com-grey?logo=Gmail)
  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   Python 3.12.4
*   JavaScript (Chrome Extension)

<h2>🛡️ License:</h2>

This project is licensed under the MIT license.

<h2>💖Like my work?</h2>

Hello if you are reading here right now it means you want to support me. Thank you very much for this kind offer but since im slightly new to github best support for me right now would be to follow my github and give a star. Thank you :)
