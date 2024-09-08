<h1 align="center" id="title">YouTube Music Github Profile</h1>

<p id="description">This project displays the song you are currently listening to on YouTube Music in real-time on your GitHub profile.</p>

<p align="center"><img src="https://img.shields.io/badge/Currently-Working-brightgreen" alt="shields"><img src="https://img.shields.io/badge/Version-1.1-blue" alt="shields"></p>

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   The project continuously monitors and displays the song you're currently listening to on YouTube Music directly on your GitHub profile. It updates in real-time ensuring your profile always shows the latest track.
*   When YouTube Music is not running or the application is offline the project gracefully switches to a default message or image indicating that no song is currently being played.
*   As an open-source project it encourages community contributions allowing users to suggest features report bugs or even develop plugins to extend its functionality.

<h2>🛠️ Installation Steps:</h2>

<p>1. Clone the project.</p>

```
git clone https://github.com/iXenonN/YouTube-Music-Profile.git
```

<p>2. Find the cloned project file in local.</p>

```
cd YouTube-Music-Profile
```

<p>3. Open app.py with your favorite Python IDE.</p>

<p>4. Install the YouTube Music api. (thanks to sigma67 for creating this api)</p>

```
pip install ytmusicapi
```

<p>5. Generate oauth.json for ytmusicapi.</p>

```
ytmusicapi oauth
```

<p>6. Create a new project in Firebase.</p>

<p>7. Download your project's Firebase Admin SDK as node.js.</p>

<p>8. Copy your Firebase project url.</p>

<p>9. Install my chrome extension for checking the YouTube Music background status.</p>

<p>10. In the cloned file install requirements.txt.</p>

```
pip install -r requirements.txt
```

<p>11. In the code change the 'YOUR OAUTH.JSON FILE' with your oauth.json file.</p>

```
ytmusic = YTMusic('YOUR OAUTH.JSON FILE')
```

<p>12. Change the 'YOUR FIREBASE CRED JSON FILE' with your firebase admin sdk json file.</p>

```
cred = credentials.Certificate('YOUR FIREBASE CRED JSON FILE')
```

<p>13. Paste your firebase project url to the 'YOUR FIREBASE PROJECT URL'.</p>

```
firebase_admin.initialize_app(cred {     'storageBucket': 'YOUR FIREBASE PROJECT URL' })
```

<p>14. Save and exit app.py.</p>

<p>15. Double click on app.py.</p>

<p>16. If you have completed all these steps successfully the code should work.</p>

<p>17. Open your profile readme.md by creating a repository with your GitHub username if you dont have already.</p>

<p>20. Go to your Firebase project.</p>

<p>21. Click the Storage tab.</p>

<p>22. Click on listening-on-ytmusic.svg file and click name then copy the url to your svg file.</p>

<p>23. Paste the text below to your profile's readme.md file:</p>

```
#
```

```
  ![What Am I Listening](your-copied-images-url)
```

<p>25. After you complete editing your readme.md file save it and go to your profile's repository.</p>

<p>26. Create a new file named update-readme.yaml into your .github/workflows folder.</p>

<p>27. Paste the code below:</p>

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
        github_token: ${{ secrets.GH_TOKEN }}
        branch: main
```

<p>28. Then save it and go to your GitHub settings.</p>

<p>32. Scroll and click Developer Settings.</p>

<p>33. Click Personal Acces Tokens and choose Tokens(classic).</p>

<p>34. Create a token gave acces to all and name whatever you want.</p>

<p>35. Copy your token.</p>

<p>36. Never share your token.</p>

<p>37. Go to settings in your profile's repository where readme.md file located.</p>

<p>38. Click secrets and variables.</p>

<p>39. Go to Actions tab.</p>

<p>40. Create a new repository secret named GH_TOKEN.</p>

<p>41. Paste your token to your repository secret named GH_TOKEN.</p>

<p>42. Save and its all done now.</p>

<h2>🍰 Contribution Guidelines:</h2>

Thank you for considering contributing to this project! To ensure a smooth and effective collaboration, please follow these guidelines:

## How to Contribute

1. **Fork the Repository**
   - Click the "Fork" button at the top right of this repository to create a copy of the repository under your GitHub account.

2. **Clone the Repository**
   - Clone your forked repository to your local machine:
     ```bash
     git clone https://github.com/your-username/repository-name.git
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

  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   Python 3.12.4
*   JavaScript (Chrome Extension)

<h2>🛡️ License:</h2>

This project is licensed under the MIT license

<h2>💖Like my work?</h2>

Hello if you are reading here right now it means you want to support me. Thank you very much for this kind offer but since I am under 18 years old I cannot work with buy me a coffe type sites so the best support for me right now would be to follow my github. Thank you :)
